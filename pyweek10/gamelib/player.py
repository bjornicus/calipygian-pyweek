'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet

import gamestate
import levels
import data
import math

class Player(gamestate.Oscillator):
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator gamestate object.
    '''
    def __init__(self, window_height=480, window_width=640):
        gamestate.Oscillator.__init__(self)

        self.SetWindowHeight(window_height)
        self.SetWindowWidth(window_width)

        self._ShipSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('Ship.png')))
        self._ShipSprite.image.anchor_x = self._ShipSprite.image.width / 2
        self._ShipSprite.image.anchor_y = self._ShipSprite.image.height / 2
        self._ShipSprite.x = self._ShipSprite.image.anchor_x

        self._PathTimes = []
        t_cursor = 0
        while (t_cursor < levels.SECONDS_TO_CROSS_SCREEN):
            self._PathTimes.append(t_cursor)
            t_cursor += 0.1
        self._PathSprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('Path.png')))
        self._PathSprite.image.anchor_x = self._PathSprite.image.width / 2
        self._PathSprite.image.anchor_y = self._PathSprite.image.height / 2

    def SetWindowHeight(self, window_height):
        self._WindowHeight = window_height

    def SetWindowWidth(self, window_width):
        self._WindowWidth = window_width

    def Tick(self, delta_t, KeyState):
        shipPos = self.GetPosition()
        shipPosInWindow = self._WindowHeight//2 + (shipPos * self._WindowHeight//2)
        self._ShipSprite.y = shipPosInWindow
        self._ShipSprite.rotation = -self.GetAngle()
        
        new_times = []
        for oldTime in self._PathTimes:
            newTime = oldTime - delta_t
            if newTime <= 0:
                newTime += levels.SECONDS_TO_CROSS_SCREEN
            new_times.append(newTime)
        self._PathTimes = new_times

        gamestate.Oscillator.Tick(self, delta_t, KeyState)

    def draw(self):

        for time in self._PathTimes:
            t, y, a = self.GetPredictiveCordinate(time)
            offset = self._WindowWidth * (t/levels.SECONDS_TO_CROSS_SCREEN)
            self._PathSprite.y = self._WindowHeight//2 + (y * self._WindowHeight//2)
            self._PathSprite.x = offset
            self._PathSprite.rotation = -a
            self._PathSprite.draw()

        self._ShipSprite.draw()