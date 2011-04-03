import pyglet
from pyglet import clock
from spaces import *

UPDATE_RATE = 60 #Update GameState logic 60 times per second
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 360
PUZZLE_BLOCK_SIDE_PIXEL_LENGTH = 90
PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH = 30
PUZZLE_BLOCK_SIDE_TILE_LENGTH = (
        PUZZLE_BLOCK_SIDE_PIXEL_LENGTH/PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH )

DefaultGameSpace = CordinateSpace()

class TestLabel(GameObject):
    GameObjectType = "Label"
    
    def __init__(self):
        GameObject.__init__(self)
        self.label = pyglet.text.Label('Hello, world', 
                                        font_name='Times New Roman', 
                                        font_size=36,
                                        color=(0,0,0,255),
                                        anchor_x='center', anchor_y='center')

    def Draw(self, xy_pos):
        self.label.x, self.label.y = xy_pos
        self.label.draw()

class Playfield(CordinateSpace):
    GameObjectType = "Playfield"
    
    def __init__(self, ResourceName):
        CordinateSpace.__init__(self)
        self.image = pyglet.resource.image(ResourceName)

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.image.blit(x,y)

class PuzzleBlock(CordinateSpace):
    PuzzleBlock = "PuzzleBlock"

    def __init__(self, solution_image):
        CordinateSpace.__init__(self)
        solution_tiles = pyglet.image.ImageGrid(
                solution_image, 
                PUZZLE_BLOCK_SIDE_TILE_LENGTH,
                PUZZLE_BLOCK_SIDE_TILE_LENGTH)

        solution_tiles_texture_grid = solution_tiles.get_texture_sequence()

        for x in range (0, PUZZLE_BLOCK_SIDE_TILE_LENGTH):
            for y in range(0,PUZZLE_BLOCK_SIDE_TILE_LENGTH):
                self.AddObject(
                        PuzzleElement(solution_tiles_texture_grid[y,x]),
                        x*PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH, 
                        y*PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH)

class PuzzleElement(GameObject):
    GameObjectType = "PuzzleElement"
    
    def __init__(self, sprite_texture_region):
        GameObject.__init__(self)
        self.sprite = sprite_texture_region

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.blit(x,y)

class PlatformElement(GameObject):
    GameObjectType = "PlatformElement"

    def __init__(self, SpriteName):
        GameObject.__init__(self)
        self.Sprite = pyglet.resource.image(SpriteName)

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.Sprite.blit(x,y)

class GrassBlock(PlatformElement):
    GameObjectType = "GrassBlock"

    def __init__(self):
        PlatformElement.__init__(self, 'Grass_Block.png')

class PlayerBlock(PlatformElement):
    GameObjectType = "PlayerBlock"

    def __init__(self):
        PlatformElement.__init__(self, 'Player_Block.png')

    def Update(self, delta_t):
        cord = self.GetCordinatesInParentSpace()
        cord.set_x(cord.get_x() + (20 * delta_t))
        
    
def run():
    pyglet.resource.path = ['data','design']
    pyglet.resource.reindex()

    setup_platformer()
    setup_puzzles()

    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    @window.event
    def on_draw():
        window.clear()
        for GameObj in DefaultGameSpace:
            cord = DefaultGameSpace.GetCordinatesOfContainedObject(GameObj)
            #here we can insert the logic for scaling!
            if cord is not None:
                GameObj.Draw((cord.get_x(), cord.get_y()))

    def update(dt):
        DefaultGameSpace.Update(dt)

    clock.schedule_interval_soft(update, 1.0 / UPDATE_RATE)
        
    pyglet.app.run()

def setup_puzzles():
    PuzzleSpace = Playfield('Puzzle_Playfield.png')
    puzzle_images = [
            pyglet.resource.image('one.png'),
            pyglet.resource.image('two.png'),
            pyglet.resource.image('three.png'),
            pyglet.resource.image('four.png'),
            pyglet.resource.image('five.png'),
            pyglet.resource.image('six.png'),
            pyglet.resource.image('seven.png'),
            pyglet.resource.image('eight.png'),
            pyglet.resource.image('nine.png')
            ]
    image_index = 0
    for x in range(0, WINDOW_WIDTH, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH):
        PuzzleSpace.AddObject(PuzzleBlock(puzzle_images[image_index]), x, 0)
        image_index += 1

    DefaultGameSpace.AddObject(PuzzleSpace, 0, 0)

def setup_platformer():
    PlatformSpace = Playfield('Platformer_Playfield.png')
    for x in range(0, WINDOW_WIDTH, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH):
        PlatformSpace.AddObject(GrassBlock(), x, 0)
    PlatformSpace.AddObject(PlayerBlock(), 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)

    DefaultGameSpace.AddObject(PlatformSpace, 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)

