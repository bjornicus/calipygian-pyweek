from spaces import *
import platformer
from constants import *
import pyglet
import random


def setup_puzzles():
    puzzlespace = CordinateSpace()
    puzzlespace.width = WINDOW_WIDTH
    puzzlespace.height = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH

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
        puzzlespace.AddObject(PuzzleBlock(puzzle_images[image_index]), x, 0)
        image_index += 1

    return puzzlespace


class PuzzleElement(GameObject):
    GameObjectType = "PuzzleElement"
    
    def __init__(self, sprite_texture_region):
        GameObject.__init__(self)
        self.selected = False
        self.sprite = pyglet.sprite.Sprite(sprite_texture_region)
        self.width = self.sprite.width
        self.height = self.sprite.height
        self.gestures = []

    def Draw(self, xy_pos):
        if (self.selected):
            self.sprite.color = (0,128,0)
        else:
            self.sprite.color = (255,255,255)
        self.sprite.x, self.sprite.y = xy_pos
        self.sprite.draw()

    def Update(self, delta_t):
        self.selected=False
        for gesture in self.gestures:
            if ((gesture.state is MOUSE_GESTURE_ABORTED) or
                (gesture.state is MOUSE_GESTURE_COMPLETED)):
                self.gestures.remove(gesture)
            else:
                if(self.TestCordIsWithinObject(gesture.depress_cord)):
                    self.selected = True
                if(self.TestCordIsWithinObject(gesture.current_cord)):
                    self.selected = True
                        
    def on_mouse_event(self, Event_Type, Chord, buttons, modifiers, gesture):
        if gesture is not None:
            self.gestures.append(gesture)


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
 

