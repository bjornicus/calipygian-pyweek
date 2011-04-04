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

    return platforspace


class Tile(GameObject):
    GameObjectType = "Tile"

    def __init__(self, SpriteName):
        GameObject.__init__(self)
        self.Sprite = pyglet.resource.image(SpriteName)
        self.width = self.Sprite.width
        self.height = self.Sprite.height

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.Sprite.blit(x,y)

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

class Player(GameObject):
    GameObjectType = "Player"

    def __init__(self):
        GameObject.__init__(self)

    def Update(self, delta_t):
        cord = self.GetCordinatesInParentSpace()
        cord.set_x(cord.get_x() + (20 * delta_t))
