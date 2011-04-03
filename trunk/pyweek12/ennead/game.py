import pyglet
from pyglet import clock
from spaces import *

import random
import platformer
import puzzle

UPDATE_RATE = 60 #Update GameState logic 60 times per second
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 360
PUZZLE_BLOCK_SIDE_PIXEL_LENGTH = 90
PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH = 30
PUZZLE_BLOCK_SIDE_TILE_LENGTH = (
        PUZZLE_BLOCK_SIDE_PIXEL_LENGTH/PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH )

DefaultGameSpace = CordinateSpace()

class Playfield(CordinateSpace):
    GameObjectType = "Playfield"
    
    def __init__(self, ResourceName):
        CordinateSpace.__init__(self)
        self.image = pyglet.resource.image(ResourceName)
        self.width = self.image.width
        self.heigh = self.image.height

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.image.blit(x,y)

class PuzzleBlock(CordinateSpace):
    PuzzleBlock = "PuzzleBlock"

    def __init__(self, solution_image):
        CordinateSpace.__init__(self)
        self.width = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
        self.heigh = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
        solution_tiles = pyglet.image.ImageGrid(
                solution_image, 
                PUZZLE_BLOCK_SIDE_TILE_LENGTH,
                PUZZLE_BLOCK_SIDE_TILE_LENGTH)

        solution_tile_list = []
        for tile in solution_tiles.get_texture_sequence():
            solution_tile_list.append(tile)

        random.shuffle(solution_tile_list)

        for x in range (0, PUZZLE_BLOCK_SIDE_TILE_LENGTH):
            for y in range(0,PUZZLE_BLOCK_SIDE_TILE_LENGTH):
                self.AddObject(
                        puzzle.PuzzleElement(solution_tile_list.pop()),
                        x*PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH, 
                        y*PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH)

class GrassBlock(platformer.PlatformElement):
    GameObjectType = "GrassBlock"

    def __init__(self):
        platformer.PlatformElement.__init__(self, 'Grass_Block.png')

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
    PlatformSpace.AddObject(platformer.PlayerBlock(), 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)

    DefaultGameSpace.AddObject(PlatformSpace, 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)

