from spaces import *
import platformer
from game import WINDOW_WIDTH
import pyglet
import random


PUZZLE_BLOCK_SIDE_PIXEL_LENGTH = 90
PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH = 30
PUZZLE_BLOCK_SIDE_TILE_LENGTH = (
        PUZZLE_BLOCK_SIDE_PIXEL_LENGTH/PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH )

def setup_puzzles(gamespace):
    PuzzleSpace = CordinateSpace()
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

    gamespace.AddObject(PuzzleSpace, 0, 0)


class PuzzleElement(GameObject):
    GameObjectType = "PuzzleElement"
    
    def __init__(self, sprite_texture_region):
        GameObject.__init__(self)
        self.sprite = sprite_texture_region

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.blit(x,y)


class PuzzleBlock(CordinateSpace):
   PuzzleBlock = "PuzzleBlock"

   def __init__(self, solution_image):
       CordinateSpace.__init__(self)
       self.width = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
       self.height = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
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
                       PuzzleElement(solution_tile_list.pop()),
                       x*PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH,
                       y*PUZZLE_ELEMENT_SIDE_PIXEL_LENGTH)
 

