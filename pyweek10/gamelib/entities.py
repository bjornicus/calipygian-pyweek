
import pyglet

from globals import *
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
        self._x = self._x - (self._WindowWidth * (delta_t / levels.SECONDS_TO_CROSS_SCREEN))
        
        rock_label.x = self._x
        rock_label.y = self._y
            
        if self._x <= 0:
            del self
        
    def draw(self):
        rock_label.draw()


class HostileShip(gamestate.Actor):

    def __init__(self, starting_x, starting_y, parent_level):
        gamestate.Actor.__init__(self, parent_level)

        self._x = starting_x
        self._y = starting_y

        self._ShipSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('Ship.png')))
        self._ShipSprite.image.anchor_x = self._ShipSprite.image.width / 2
        self._ShipSprite.image.anchor_y = self._ShipSprite.image.height / 2
        self._ShipSprite.x = self._ShipSprite.image.anchor_x
        self._ShipSprite.color = (128,0,0)
        self._ShipSprite.rotation = 180

        self._PathSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('Path.png')))
        self._PathSprite.image.anchor_x = self._PathSprite.image.width / 2
        self._PathSprite.image.anchor_y = self._PathSprite.image.height / 2
        self._PathSprite.color = (128,0,0)

    def Tick(self, delta_t):
        self._x = self._x - (self._WindowWidth * (delta_t / levels.SECONDS_TO_CROSS_SCREEN))
            
        self._ShipSprite.x = self._x
        self._ShipSprite.y = self._y 
        
        gamestate.Actor.Tick(self, delta_t)
        
        if self._x <= 0:
            del self
        
    def draw(self):
        gamestate.Actor.draw(self)
        self._ShipSprite.draw()