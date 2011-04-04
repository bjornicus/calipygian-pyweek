import pyglet
from spaces import GameObject, CordinateSpace
from game import WINDOW_HEIGHT, WINDOW_WIDTH 
from puzzle import PUZZLE_BLOCK_SIDE_PIXEL_LENGTH


def setup_platformer(gamespace):
    PlatformSpace = CordinateSpace()
    PlatformSpace.width = WINDOW_WIDTH
    PlatformSpace.height = WINDOW_HEIGHT - PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
    
    for x in range(0, WINDOW_WIDTH, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH):
        PlatformSpace.AddObject(GrassBlock(), x, 0)
    PlatformSpace.AddObject(PlayerBlock(), 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)

    gamespace.AddObject(PlatformSpace, 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)


class PlatformElement(GameObject):
    GameObjectType = "PlatformElement"

    def __init__(self, SpriteName):
        GameObject.__init__(self)
        self.Sprite = pyglet.resource.image(SpriteName)
        self.width = self.Sprite.width
        self.height = self.Sprite.height

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
