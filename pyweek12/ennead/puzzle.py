from spaces import *


class PuzzleElement(GameObject):
    GameObjectType = "PuzzleElement"
    
    def __init__(self, sprite_texture_region):
        GameObject.__init__(self)
        self.sprite = sprite_texture_region

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.blit(x,y)
