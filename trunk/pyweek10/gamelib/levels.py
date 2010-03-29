'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet
from pyglet.window import key

import gamestate
import random
import player

SECONDS_TO_CROSS_SCREEN = 2

##FIXME Temporary testing hacks Remove these!
playership = player.Player()
shiplabel = pyglet.text.Label('Ship', x=0, y=240)
predictive_label = pyglet.text.Label('-')
rock_label = pyglet.text.Label('ROCK!')
rocks = []

##End of FIXME

class LevelBase(object):
    '''
    A base class for game levels
    '''
    def __init__(self, window):
        '''
        Create a level that runs in the given window
        '''
        self.window = window
        self.keystate = pyglet.window.key.KeyStateHandler()
        self.renderlist = []
        self.actorlist = []
        self.reactorlist = [] # list of objects expecting to pool keyboard state when they update
        self.fps_display = pyglet.clock.ClockDisplay()

        playership.SetWindowHeight(self.window.height)

        self.renderlist.append(playership)
        self.renderlist.append(self.fps_display)
        self.reactorlist.append(playership)

        self.window.push_handlers(self.keystate)
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def on_draw(self):
        self.window.clear()
        for drawable in self.renderlist:
            drawable.draw()

    def update(self, dt):
        for actor in self.actorlist:
            actor.Tick(dt)
        for reactor in self.reactorlist:
            reactor.Tick(dt, self.keystate)

        ## Hacks
        for rock in rocks:
            rock["x"] = rock["x"] - ((dt/SECONDS_TO_CROSS_SCREEN)* self.window.width)
            if rock["x"] < 0:
                rocks.remove(rock)
        rockprob = random.randrange(100)
        if (rockprob > 95) and (len(rocks) < 5):
            rocks.append({"x":self.window.width, "y":random.randrange(self.window.height)})

class LevelOne(LevelBase):
    '''
    Level One
    '''
    def __init__(self, window):
        LevelBase.__init__(self, window)

    def on_draw(self):
        LevelBase.on_draw(self)

        for rock in rocks:
            rock_label.x = rock["x"]
            rock_label.y = rock["y"]
            rock_label.draw()