import pyglet
from pyglet import clock
from spaces import *

UPDATE_RATE = 60 #Update GameState logic 60 times per second

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

    def __init__(self):
        CordinateSpace.__init__(self)
        ElementSprites = ['Puzzle_A.png', 'Puzzle_B.png', 'Puzzle_C.png']
        for x in range(0,90,30):
            for y in range (0, 90, 30):
                self.AddObject(PuzzleElement(ElementSprites), x, y)

class PuzzleElement(GameObject):
    GameObjectType = "PuzzleElement"
    
    def __init__(self, SpriteNames):
        GameObject.__init__(self)
        self.SpriteSequence = []
        for SpriteName in SpriteNames:
            self.SpriteSequence.append(pyglet.resource.image(SpriteName))

        self.CurrentSprite = self.SpriteSequence[0]

    def NextSprite(self):
        if self.CurrentSprite not in self.SpriteSequence:
            self.CurrentSprite = self.SpriteSequence[0]

        i = self.SpriteSequence.Index(self.CurrentSprite)
        self.CurrentSprite = self.SpriteSequence[(i+1)% len(self.SpriteSequence)]

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.CurrentSprite.blit(x,y)

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
    window = pyglet.window.Window(810, 360)

    pyglet.resource.path = ['data','design']
    pyglet.resource.reindex()

    setup_platformer()

    setup_puzzles()

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
    for x in range(0, 810, 90):
        PuzzleSpace.AddObject(PuzzleBlock(), x, 0)
    DefaultGameSpace.AddObject(PuzzleSpace, 0, 0)

def setup_platformer():
    PlatformSpace = Playfield('Platformer_Playfield.png')
    for x in range(0, 810, 90):
        PlatformSpace.AddObject(GrassBlock(), x, 0)
    PlatformSpace.AddObject(PlayerBlock(), 0, 90)

    DefaultGameSpace.AddObject(PlatformSpace, 0, 90)

