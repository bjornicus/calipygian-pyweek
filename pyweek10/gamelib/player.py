'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet
from pyglet.window import key

import gamestate
import levels
import random
import data
import math

class Player(gamestate.Oscillator):
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator gamestate object.
    '''
    def __init__(self, window_height=480):
        gamestate.Oscillator.__init__(self)

        self.SetWindowHeight(window_height)
        self._ShipSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('Ship.png')))
        self._ShipSprite.image.anchor_x = self._ShipSprite.image.width // 2
        self._ShipSprite.image.anchor_y = self._ShipSprite.image.height // 2
        self._ShipSprite.x = self._ShipSprite.image.anchor_x

    def SetWindowHeight(self, window_height):
        self.WindowHeight = window_height

    def Tick(self, delta_t, KeyState):
        shipPos = self.GetPosition()
        shipPosInWindow = self.WindowHeight//2 + (shipPos * self.WindowHeight//2)
        self._ShipSprite.y = shipPosInWindow
        self._ShipSprite.rotation = -math.cos(self.GetAngle()) * 45

        gamestate.Oscillator.Tick(self, delta_t, KeyState)

    def draw(self):
        self._ShipSprite.draw()