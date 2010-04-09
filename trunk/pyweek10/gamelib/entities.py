import pyglet

from constants import *
import levels
import random
import data
import math
from collide import *
from pyglet.window import key

if DEBUG:
    import debug

class Entity(object):
    '''
    An entity is anything in the game that gets updated 
    '''
    entity_type = None
    def __init__(self, parent_level, layer = 2):
        self.parent_level = parent_level

        self._scaleFactor = 1
        self._x_offset = 0
        self._y_offset = 0

        self.parent_level.register_entity(self, layer, self.entity_type)

    def Rescale(self, NewScaleFactor):
        self._scaleFactor = NewScaleFactor

    def SetOffsets(self, x, y):
        self._x_offset = x
        self._y_offset = y

    def GetScaledX(self, x):
        return x * self._scaleFactor + self._x_offset

    def GetScaledY(self, y):
        return y * self._scaleFactor + self._y_offset

    def delete(self):
        self.parent_level.remove_entity(self, self.entity_type)

    def draw(self):
        pass

    def update(self, delta_t):
        pass

class Actor(Entity):
    '''
    Actors are entities that have an associated sprite
    '''
    entity_type = None
    def __init__(self, sprite_image, parent_level, layer = 2):
        self.sprite = pyglet.sprite.Sprite(sprite_image)
        self.collider = SpriteCollision(self.sprite) 
        Entity.__init__(self, parent_level, layer)

    def Rescale(self, NewScaleFactor):
        Entity.Rescale(self, NewScaleFactor)
        self.sprite.scale = float(NewScaleFactor)

    def draw(self):
        self.sprite.draw()

    # Return the sprite for this entity, if any
    def get_collidable(self):
        pass

class HostileShip(Actor):

    entity_type = TYPE_HOSTILE_SHIP
    def __init__(self, starting_x, starting_y, speed, parent_level, sprite_number = 1):
        if sprite_number == 1:
            sprite_image = data.load_image('Enemy1.png')
        elif sprite_number == 2:
            sprite_image = data.load_image('Enemy2.png')
        elif sprite_number == 3:
            sprite_image = data.load_image('Enemy3.png')
        elif sprite_number == 3:
            sprite_image = data.load_image('Enemy4.png')
        else:
            sprite_image = data.load_image('enemy.png')

        sprite_image.anchor_y = sprite_image.height/2  
        Actor.__init__(self, sprite_image, parent_level)

        self._x = starting_x
        self._y = starting_y
        self.speed = speed

    def Rescale(self, NewScaleFactor):
        Actor.Rescale(self, NewScaleFactor)
        self.sprite.scale = float(NewScaleFactor)

    def update(self, delta_t):
        self._x = self._x - (SIZE_OF_GAMESPACE_X * (delta_t / SECONDS_TO_CROSS_GAMESPACE) + (self.speed * delta_t/abs(delta_t)))

        Actor.update(self, delta_t)

        if self._x <= 0:
            self.delete()

    def draw(self):
        self.sprite.x = self.GetScaledX(self._x)
        self.sprite.y = self.GetScaledY(self._y)
        Actor.draw(self)
        if DEBUG:
            debug.draw_bounding_box(self.sprite)

    def get_collidable(self):
        return SpriteCollision(self.sprite) 

class CollidableTerrain(Entity):
    '''
    A class to manage our foreground terrain
    '''
    entity_type = TYPE_TERRAIN

    def __init__(self, filename, parent_level, layer = 2, scrolling_factor = 1.0):
        print 'loading terrain...'
        self.image = pyglet.image.load(data.filepath(filename))
        self._ImagePieces = []
        self._Colliders = []
        self._scale = (float(SIZE_OF_GAMESPACE_Y) / float(self.image.height))
        Entity.__init__(self, parent_level, layer=layer)

        x = 0
        while x < self.image.width:
            width = min(WIDTH_OF_TERRAIN_SLICE, self.image.width - x)
            ImagePiece = self.image.get_region(x, 0, width, self.image.height)
            sprite = pyglet.sprite.Sprite(ImagePiece)
            sprite.x = self.GetScaledX(x)
            sprite.scale = self._scale
            self._ImagePieces.append(sprite)
            x += width

        print 'loading collision data...'
        for piece in self._ImagePieces:
            collider = SpriteCollision(piece)
            collider.get_image() #pre-cache the collision pixel data
            self._Colliders.append(collider)
        self.x = 0
        self.y = 0

        self._scrolling_factor = scrolling_factor

    def reset(self):
        x = 0
        for sprite in self._ImagePieces:
            width = min(WIDTH_OF_TERRAIN_SLICE, self.image.width - x)
            sprite.x = self.GetScaledX(x)
            sprite.scale = self._scale
            x += width


    def Rescale(self, NewScaleFactor):
        super(CollidableTerrain, self).Rescale(NewScaleFactor)
        self._scale = float(NewScaleFactor) * (float(SIZE_OF_GAMESPACE_Y) / float(self.image.height))
        for sprite in self._ImagePieces:
            sprite.scale = self._scale
        self.scaled_gamespace_width = self.GetScaledX(SIZE_OF_GAMESPACE_X)
        self.scaled_image_width = self.GetScaledX(self.image.width)

    def update(self, dt):
        dx = (self.scaled_gamespace_width * (dt / SECONDS_TO_CROSS_GAMESPACE)) * self._scrolling_factor
        for sprite in self._ImagePieces:
            sprite.x -= dx
            if (sprite.x + sprite.width < 0):
                sprite.x += self.scaled_image_width

        super(CollidableTerrain, self).update(dt)

    def draw(self):
        for sprite in self._ImagePieces:
            if sprite.x + sprite.width > 0 and sprite.x < self.scaled_gamespace_width:
                sprite.draw()
                if DEBUG:
                    debug.draw_bounding_box(sprite)
        super(CollidableTerrain, self).draw()


    def collide(self,collideable):
        #return False
        for piece in self._ImagePieces:
            if collide(collideable, SpriteCollision(piece)):
                return True
        return False

class Debris(Actor):
    entity_type = TYPE_DEBRIS
    def __init__(self, starting_x, starting_y, parent_level):
        # this should mb come in as a parameter 
        # or we should choose at random, but we need to know from what set
        sprite_image = data.load_image('Level1Debris1.png')
        sprite_image.anchor_x = sprite_image.width/2
        sprite_image.anchor_y = sprite_image.height/2
        Actor.__init__(self, sprite_image, parent_level)
        self.x = starting_x
        self.y = starting_y
        self.vx = 0
        self.vy = 0

    def update(self, dt):
        self.x = self.x - (SIZE_OF_GAMESPACE_X * (dt / SECONDS_TO_CROSS_GAMESPACE))

    def draw(self):
        self.sprite.x = self.GetScaledX(self.x)
        self.sprite.y = self.GetScaledY(self.y)
        Actor.draw(self)

    def get_collidable(self):
        return SpriteCollision(self.sprite)

