
import pyglet

import gamestate
import levels
import random
import data
import math

class HostleShip():
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator gamestate object.
    '''
    def __init__(self, starting_x, starting_y, level_base):

        self.parent_level = level_base
        
        self.SetWindowHeight(self.parent_level.window.height)
        self.SetWindowWidth(self.parent_level.window.width)
        
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
        
    def __del__(self):
        self.parent_level.remove_entity(self)

    def SetWindowHeight(self, window_height):
        self._WindowHeight = window_height

    def SetWindowWidth(self, window_width):
        self._WindowWidth = window_width

    def Tick(self, delta_t):
        self._x = self._x - (self._WindowWidth * (delta_t / levels.SECONDS_TO_CROSS_SCREEN))
            
        self._ShipSprite.x = self._x
        self._ShipSprite.y = self._y 
        
        if self._x <= 0:
            del self
        

    def draw(self):

        """
        for (t, y, a) in self.GetPredictivePath(.1, levels.SECONDS_TO_CROSS_SCREEN, .1):
            offset = self._WindowWidth * (t/levels.SECONDS_TO_CROSS_SCREEN)
            self._PathSprite.y = self._WindowHeight//2 + (y * self._WindowHeight//2)
            self._PathSprite.x = offset
            self._PathSprite.rotation = -a
            self._PathSprite.draw()
        """

        self._ShipSprite.draw()