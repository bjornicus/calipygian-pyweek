import pyglet
from spaces import *


class PlatformElement(GameObject):
    GameObjectType = "PlatformElement"

    def __init__(self, SpriteName):
        GameObject.__init__(self)
        self.Sprite = pyglet.resource.image(SpriteName)

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.Sprite.blit(x,y)
class PlayerBlock(PlatformElement):
    GameObjectType = "PlayerBlock"

    def __init__(self):
        PlatformElement.__init__(self, 'Player_Block.png')

    def Update(self, delta_t):
        cord = self.GetCordinatesInParentSpace()
        cord.set_x(cord.get_x() + (20 * delta_t))
