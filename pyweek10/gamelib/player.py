'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet
from entities import *
from constants import *
import levels
import data
import math

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
        self._ShipSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/Ship.png')))
        self._ShipSprite.image.anchor_x = self._ShipSprite.image.width
        self._ShipSprite.image.anchor_y = self._ShipSprite.image.height / 2
        
        self._PathSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/Path.png')))
        self._PathSprite.image.anchor_x = self._PathSprite.image.width / 2
        self._PathSprite.image.anchor_y = self._PathSprite.image.height / 2
        
        Oscillator.__init__(self)
        Reactor.__init__(self, parent_level)
        
        self._x = PLAYER_OFFFSET_FROM_RIGHT_SCREEN_BOUND
        self._y = SIZE_OF_GAMESPACE_Y//2
        
        self._original_color = self._ShipSprite.color

        self._PathTimes = []
        t_cursor = 0
        while (t_cursor < SECONDS_TO_CROSS_GAMESPACE):
            self._PathTimes.append(t_cursor)
            t_cursor += float(SECONDS_TO_CROSS_GAMESPACE) / PATH_POINTS

        
    def Rescale(self, NewScaleFactor):
        Reactor.Rescale(self, NewScaleFactor)
        self._ShipSprite.scale = float(NewScaleFactor)
        self._PathSprite.scale = float(NewScaleFactor)


    def Tick(self, delta_t, KeyState):
        shipPos = self.GetCurrentValue()
        self._y  = SIZE_OF_GAMESPACE_Y//2 + (shipPos * SIZE_OF_GAMESPACE_Y//2)
        new_times = []
        for oldTime in self._PathTimes:
            newTime = oldTime - delta_t
            if newTime <= 0:
                newTime += SECONDS_TO_CROSS_GAMESPACE
            new_times.append(newTime)
        self._PathTimes = new_times

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
        

    def draw(self):
        self._ShipSprite.x = self.GetScaledX(self._x)
        self._ShipSprite.y = self.GetScaledY(self._y)
        self._ShipSprite.rotation = -self.GetAngle()
        
        for time in self._PathTimes:
            t, y, a = self.GetPredictiveCoordinate(time)
            offset = SIZE_OF_GAMESPACE_X * t/float(SECONDS_TO_CROSS_GAMESPACE) + self._x
            self._PathSprite.y = self.GetScaledY(SIZE_OF_GAMESPACE_Y//2 + (y * SIZE_OF_GAMESPACE_Y//2))
            self._PathSprite.x = self.GetScaledX(offset)
            self._PathSprite.rotation = -a
            self._PathSprite.draw()

        self._ShipSprite.draw()
        Reactor.draw(self)
