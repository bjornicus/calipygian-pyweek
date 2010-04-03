'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet
from pyglet.window import key
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


class Player(Actor, Oscillator):
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator object.
    '''
    def __init__(self, parent_level):
        sprite_image = data.load_image('Ship.png')
        sprite_image.anchor_y = sprite_image.height/2  
        Actor.__init__(self, sprite_image, parent_level)
        Oscillator.__init__(self)
        self.x = PLAYER_OFFFSET_FROM_RIGHT_SCREEN_BOUND
        self.y = SIZE_OF_GAMESPACE_Y//2
        self.z = 1 #draw this above other stuff
        
        self._original_color = self.sprite.color

        
    def Rescale(self, NewScaleFactor):
        super(Player, self).Rescale(NewScaleFactor)

    def Tick(self, delta_t):
        Oscillator.Tick(self, delta_t)
        shipPos = self.GetCurrentValue()
        self.y  = SIZE_OF_GAMESPACE_Y//2 + (shipPos * SIZE_OF_GAMESPACE_Y//2)
    
    def handle_input(self, keys):
        if keys[key.UP] and not keys[key.DOWN]:
            self.AmplitudeAdjust = INCREASE
        elif keys[key.DOWN] and not keys[key.UP]:
            self.AmplitudeAdjust = DECREASE
        else:
            self.AmplitudeAdjust = CONSTANT

        if keys[key.RIGHT] and not keys[key.LEFT]:
            self.FrequencyAdjust = INCREASE
        elif keys[key.LEFT] and not keys[key.RIGHT]:
            self.FrequencyAdjust = DECREASE
        else:
            self.FrequencyAdjust = CONSTANT

        if keys[key.SPACE]:
            self.frozen = True
        else: 
            self.frozen = False

    def get_hitbox(self):
        # TODO: make this hit box smaller
        return (self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height)
    
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
            self.sprite.color = (255,0,0)
        else:
            self.sprite.color = self._original_color
        
        return collision
        
    def reset_color(self):
        self.sprite.color = self._original_color

    def draw(self):
        self.sprite.x = self.GetScaledX(self.x)
        self.sprite.y = self.GetScaledY(self.y)
        self.sprite.rotation = -self.GetAngle()
        self.draw_path()
        self.sprite.draw()
        if DEBUG:
            draw_bounding_box(self.sprite)
        
    def draw_path(self):
        glColor4f(0.75, 0.75, 1, 1) 
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        for time in arange(0, SECONDS_TO_CROSS_GAMESPACE, 0.2/self._Omega):
            t, y, a = self.GetPredictiveCoordinate(time)
            x = self.GetScaledX(SIZE_OF_GAMESPACE_X * t/float(SECONDS_TO_CROSS_GAMESPACE) + self.x )
            y = self.GetScaledY(SIZE_OF_GAMESPACE_Y//2 + (y * SIZE_OF_GAMESPACE_Y//2))
            glVertex2f(x,y)
        glEnd()
        glLineWidth(1)
        glColor4f(1, 1, 1, 1) 

