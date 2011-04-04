import pyglet
from spaces import GameObject, CordinateSpace
from constants import *

TILE_SIZE_IN_PIXELS = 30
LEVEL_WIDTH_IN_TILES = 27
LEVEL_HEIGHT_IN_TILES = 9

def setup_platformer():
    platforspace = CordinateSpace()
    platforspace.width = LEVEL_WIDTH_IN_TILES * TILE_SIZE_IN_PIXELS
    platforspace.height = LEVEL_HEIGHT_IN_TILES * TILE_SIZE_IN_PIXELS
    
    for x in range(0, LEVEL_WIDTH_IN_TILES):
        for y in range(0, LEVEL_HEIGHT_IN_TILES):
            tyle_type = level_map[y][x]
            x_coord = x * TILE_SIZE_IN_PIXELS
            y_coord = y * TILE_SIZE_IN_PIXELS
            platforspace.AddObject(level_map_key[tyle_type](), x_coord, y_coord)
    platforspace.AddObject(Player(), TILE_SIZE_IN_PIXELS, 3*TILE_SIZE_IN_PIXELS)

    return platforspace


class Tile(GameObject):
    GameObjectType = "Tile"

    def __init__(self, sprite_name):
        GameObject.__init__(self)
        self.sprite = pyglet.resource.image(sprite_name)
        self.width = self.sprite.width
        self.height = self.sprite.height

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.blit(x,y)

class EmptyTile(GameObject):
    GameObjectType = "Empty"

    def __init__(self):
        GameObject.__init__(self)

class Grass(Tile):
    GameObjectType = "Grass"

    def __init__(self):
        Tile.__init__(self, 'grass.png')

class Dirt(Tile):
    GameObjectType = "Dirt"

    def __init__(self):
        Tile.__init__(self, 'dirt.png')

level_map_key = { 0:EmptyTile, 1:Grass, 2:Dirt }

level_map = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,2,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,1]
        ]
level_map.reverse()

def find_tile_for_point(x,y):
    x = int(x / TILE_SIZE_IN_PIXELS)
    y = int(y / TILE_SIZE_IN_PIXELS)
    return level_map[y][x]

class Player(GameObject):
    GameObjectType = "Player"

    def __init__(self):
        GameObject.__init__(self)
        self.sprite = pyglet.resource.image('player.png')

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.blit(x,y)

    def Update(self, delta_t):
        cord = self.GetCordinatesInParentSpace()
        x,y = cord.get_x(), cord.get_y()
        lower_left_tile = find_tile_for_point(x,y)
        lower_right_tile = find_tile_for_point(x+TILE_SIZE_IN_PIXELS,y)
        if lower_left_tile == 0 and lower_right_tile == 0:
            cord.set_y(cord.get_y() - (20 * delta_t))

        cord.set_x(cord.get_x() + (20 * delta_t))
