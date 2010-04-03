'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet
from pyglet.gl import *
from entities import *
from constants import *
import levels
import data
import math
from numpy import arange
if DEBUG:
    from debug import *

PATH_POINTS = 50.0

# hit box helpers.
HITBOX_X = lambda hitbox: hitbox[0]
HITBOX_Y = lambda hitbox: hitbox[1]
HITBOX_WIDTH = lambda hitbox: hitbox[2]
HITBOX_HEIGHT = lambda hitbox: hitbox[3]


class Player(Oscillator, Reactor):
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator object.
    '''
    def __init__(self, parent_level):
        Oscillator.__init__(self)
        self._ShipSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/Ship.png')))
        self._ShipSprite.image.anchor_y = self._ShipSprite.image.height/2
        Reactor.__init__(self, parent_level)
        
        self._x = PLAYER_OFFFSET_FROM_RIGHT_SCREEN_BOUND
        self._y = SIZE_OF_GAMESPACE_Y//2
        self.z = 1 #draw this above other stuff
        
        self._original_color = self._ShipSprite.color

        
    def Rescale(self, NewScaleFactor):
        Reactor.Rescale(self, NewScaleFactor)
        self._ShipSprite.scale = float(NewScaleFactor)


    def Tick(self, delta_t, KeyState):
        shipPos = self.GetCurrentValue()
        self._y  = SIZE_OF_GAMESPACE_Y//2 + (shipPos * SIZE_OF_GAMESPACE_Y//2)
        Oscillator.Tick(self, delta_t, KeyState)
        Reactor.Tick(self, delta_t, KeyState)
    
    def get_hitbox(self):
        # TODO: make this hit box smaller
        return (self._ShipSprite.x, self._ShipSprite.y, self._ShipSprite.width, self._ShipSprite.height)
    
    def CollidedWith(self, actor):
        # TODO: this should be refined to maybe take pixels into account. 
        
        # return 1 if you collided with the actor or 0 if you did not.
        
        # figure out what the hit box of the player is
        player_hitbox = self.get_hitbox()
        
        # figure out what the hit box of the actor is
        actor_hitbox = actor.get_hitbox()
        
        # see if they collide
        collision = 0
        
        if(actor_hitbox is not None):
            if(HITBOX_X(player_hitbox) <= HITBOX_X(actor_hitbox) and \
               HITBOX_X(actor_hitbox) <= HITBOX_X(player_hitbox) + HITBOX_WIDTH(player_hitbox)):
                if(HITBOX_Y(player_hitbox) <= HITBOX_Y(actor_hitbox) and \
                   HITBOX_Y(actor_hitbox) <= HITBOX_Y(player_hitbox) + HITBOX_HEIGHT(player_hitbox)):
                    collision = 1;
        
        # print "collide! player: ", player_hitbox, " actor: ", actor_hitbox, " collision: ", collision 
        
        if collision:
            self._ShipSprite.color = (255,0,0)
        else:
            self._ShipSprite.color = self._original_color
        
        return collision
        
    def reset_color(self):
        self._ShipSprite.color = self._original_color

    def draw(self):
        self._ShipSprite.x = self.GetScaledX(self._x)
        self._ShipSprite.y = self.GetScaledY(self._y)
        self._ShipSprite.rotation = -self.GetAngle()
        self.draw_path()
        self._ShipSprite.draw()
        if DEBUG:
            draw_bounding_box(self._ShipSprite)
        
    def draw_path(self):
        #glColor4f(0.5, 0.5, 1, 1) 
        glBegin(GL_LINE_STRIP)
        for time in arange(0, SECONDS_TO_CROSS_GAMESPACE, 0.2/self._Omega):
            t, y, a = self.GetPredictiveCoordinate(time)
            x = self.GetScaledX(SIZE_OF_GAMESPACE_X * t/float(SECONDS_TO_CROSS_GAMESPACE) + self._x )
            y = self.GetScaledY(SIZE_OF_GAMESPACE_Y//2 + (y * SIZE_OF_GAMESPACE_Y//2))
            glVertex2f(x,y)
        glEnd()
        glColor4f(1, 1, 1, 1) 

