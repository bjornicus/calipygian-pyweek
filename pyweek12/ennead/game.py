UPDATE_RATE = 60 #Update GameState logic 60 times per second
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 360

import pyglet
from pyglet import clock
from spaces import CordinateSpace

import random
import platformer
import puzzle

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

def run():
    pyglet.resource.path = ['data','design']
    pyglet.resource.reindex()

    root_game_space = CordinateSpace()
    platformer.setup_platformer(root_game_space)
    puzzle.setup_puzzles(root_game_space)

    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    @window.event
    def on_draw():
        window.clear()
        for GameObj in root_game_space:
            cord = root_game_space.GetCordinatesOfContainedObject(GameObj)
            #here we can insert the logic for scaling!
            if cord is not None:
                GameObj.Draw((cord.get_x(), cord.get_y()))

    def update(dt):
        root_game_space.Update(dt)

    clock.schedule_interval_soft(update, 1.0 / UPDATE_RATE)
        
    pyglet.app.run()

