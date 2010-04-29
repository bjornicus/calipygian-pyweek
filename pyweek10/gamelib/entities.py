import pyglet
from pyglet.gl import *

from constants import *
import levels
import random
import data
import math
from numpy import arange
from collide import *
import oscillator
from pyglet.window import key
from gamelib.constants import *
from gamelib.levels import SIZE_OF_GAMESPACE_Y, SECONDS_TO_CROSS_GAMESPACE


class Entity(object):
    '''
    An entity is anything in the game that gets updated 
    '''
    entity_type = None
    def __init__(self, parent_level, layer = 2):
        self.parent_level = parent_level
        self.parent_level.register_entity(self, layer, self.entity_type)

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

    def update(self, delta_t):
        self._x = self._x - (SIZE_OF_GAMESPACE_X * (delta_t / SECONDS_TO_CROSS_GAMESPACE) + (self.speed * delta_t/abs(delta_t)))

        Actor.update(self, delta_t)

        if self._x <= 0:
            self.delete()

    def draw(self):
        self.sprite.x = self._x
        self.sprite.y = self._y
        Actor.draw(self)
        if DEBUG:
            debug.draw_bounding_box(self.sprite)

    def get_collidable(self):
        return SpriteCollision(self.sprite) 


class FullscreenScrollingSprite(Entity):
    '''
    A class to manage a full-screen scrolling sprite.
    '''
    def __init__(self, filename, parent_level, layer = 2, scrolling_factor = 1.0):
        self.Image = pyglet.image.load(data.filepath(filename))
        self._ImagePieces = []

        x = 0
        while x < self.Image.width:
            width = min(SIZE_OF_GAMESPACE_X, self.Image.width - x)
            ImagePiece = self.Image.get_region(x, 0, width, self.Image.height)
            sprite = pyglet.sprite.Sprite(ImagePiece)
            self._ImagePieces.append(sprite)
            x += width

        Entity.__init__(self, parent_level, layer=layer)
        self._scrolling_factor = scrolling_factor

        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0

    def update(self, dt):
        self.x -= (SIZE_OF_GAMESPACE_X * (dt / SECONDS_TO_CROSS_GAMESPACE)) * self._scrolling_factor
        if (self.x < -self.Image.width):
            self.x += self.Image.width

        super(FullscreenScrollingSprite, self).update(dt)

    def draw(self):
        x = int(self.x - 0.5)
        while (x + self.Image.width < SIZE_OF_GAMESPACE_X + self.Image.width):
            x_offset = x
            x_draw_offset = x_offset
            for sprite in self._ImagePieces:
                if (x_offset + sprite.image.width < 0 or x_offset > SIZE_OF_GAMESPACE_X):
                    pass
                else:
                    sprite.x = x_draw_offset
                    sprite.y = self.y
                    sprite.draw()
                x_draw_offset += int(sprite.width - .5)
                x_offset += sprite.image.width

            x += self.Image.width

        super(FullscreenScrollingSprite, self).draw()


    def get_collidable(self):
        return None

if DEBUG:
    import debug
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
        Entity.__init__(self, parent_level, layer=layer)

        x = 0
        while x < self.image.width:
            width = min(WIDTH_OF_TERRAIN_SLICE, self.image.width - x)
            ImagePiece = self.image.get_region(x, 0, width, self.image.height)
            sprite = pyglet.sprite.Sprite(ImagePiece)
            sprite.x = x
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
            sprite.x = x
            x += width

    def update(self, dt):
        dx = (SIZE_OF_GAMESPACE_X * (dt / SECONDS_TO_CROSS_GAMESPACE)) * self._scrolling_factor
        for sprite in self._ImagePieces:
            sprite.x -= dx
            if (sprite.x + sprite.width < 0):
                sprite.x += self.image.width

        super(CollidableTerrain, self).update(dt)

    def draw(self):
        for sprite in self._ImagePieces:
            if sprite.x + sprite.width > 0 and sprite.x < SIZE_OF_GAMESPACE_X:
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

class TargetPath(Entity, oscillator.Oscillator):
    def __init__(self, parent_level, layer = 2):
        Entity.__init__(self, parent_level, layer)
        oscillator.Oscillator.__init__(self)
        self.x = PLAYER_OFFFSET_FROM_RIGHT_SCREEN_BOUND
        self.y = SIZE_OF_GAMESPACE_Y//2
        self.z = 1 #draw this above other stuff
        self.line_color = (1,1,1,1)

    def draw(self):
        self.draw_path()

    def update(self, dt):
        oscillator.Oscillator.update(self, dt)
        self.y  = SIZE_OF_GAMESPACE_Y//2 + (self.GetCurrentValue() * SIZE_OF_GAMESPACE_Y//2)

    def draw_path(self):
        glColor4f(*self.line_color) 
        glLineWidth(2)
        glBegin(GL_LINES)
        for time in arange(0, SECONDS_TO_CROSS_GAMESPACE, 0.2/self._Omega):
            t, y, a = self.GetPredictiveCoordinate(time)
            x = SIZE_OF_GAMESPACE_X * t/float(SECONDS_TO_CROSS_GAMESPACE) + self.x 
            y = SIZE_OF_GAMESPACE_Y//2 + (y * SIZE_OF_GAMESPACE_Y//2)
            glVertex2f(x,y)
        glEnd()
        glLineWidth(1)
        glColor4f(1, 1, 1, 1) 

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
        self.sprite.x = self.x
        self.sprite.y = self.y
        Actor.draw(self)

    def get_collidable(self):
        return SpriteCollision(self.sprite)

