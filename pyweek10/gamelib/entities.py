
import pyglet

from constants import *
import gamestate
import levels
import random
import data
import math

class Rock(gamestate.Actor):
    rock_label = pyglet.text.Label('ROCK!')

    def __init__(self, starting_x, starting_y, parent_level):
        gamestate.Actor.__init__(parent_level)

        self._x = starting_x
        self._y = starting_y

    def Tick(self, delta_t):
        self._x = self._x - (SIZE_OF_GAMESPACE_X * (delta_t / SECONDS_TO_CROSS_GAMESPACE))

        if self._x <= 0:
            del self

    def draw(self):
        
        rock_label.x = self.GetScaledX(self._x)
        rock_label.y = self.GetScaledY(self._y)
        rock_label.draw()
    
    def get_hitbox(self):
        # TODO: make this hit box smaller
        return (self._x, self._y, self.rock_label.width, self.rock_label.height)

class HostileShip(gamestate.Actor):

    def __init__(self, starting_x, starting_y, parent_level):
        self._ShipSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/Ship.png')))
        self._ShipSprite.image.anchor_x = self._ShipSprite.image.width / 2
        self._ShipSprite.image.anchor_y = self._ShipSprite.image.height / 2
        
        gamestate.Actor.__init__(self, parent_level)

        self._x = starting_x
        self._y = starting_y

        self._ShipSprite.x = self._ShipSprite.image.anchor_x
        self._ShipSprite.color = (128,0,0)
        self._ShipSprite.rotation = 180
        
        
    def Rescale(self, NewScaleFactor):
        gamestate.Actor.Rescale(self, NewScaleFactor)
        self._ShipSprite.scale = float(NewScaleFactor)

    def Tick(self, delta_t):
        self._x = self._x - (SIZE_OF_GAMESPACE_X * (delta_t / SECONDS_TO_CROSS_GAMESPACE))

        gamestate.Actor.Tick(self, delta_t)
        
        if self._x <= 0:
            self.delete()
        
    def draw(self):
        gamestate.Actor.draw(self)
        self._ShipSprite.x = self.GetScaledX(self._x)
        self._ShipSprite.y = self.GetScaledY(self._y)
        self._ShipSprite.draw()
        
    def get_hitbox(self):
        # TODO: make this hit box smaller
        return (self._x, self._y, self._ShipSprite.width, self._ShipSprite.height)