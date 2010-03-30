'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode

import config
from common import *
from constants import *
import pyglet
from pyglet.window import key

import gamestate
import random
import player
import entities

SECONDS_TO_CROSS_SCREEN = 4

##FIXME Temporary testing hacks Remove these!
playership = player.Player()
rock_label = pyglet.text.Label('ROCK!')
rocks = []

##End of FIXME

class LevelBase(mode.Mode):
    '''
    A base class for game levels
    '''
    name = "levelbase"
    def __init__(self ):
        '''
        Create a level that runs in the given window
        '''
        super(LevelBase, self).__init__()
        self.keystate = pyglet.window.key.KeyStateHandler()
        self.renderlist = []
        self.actorlist = []
        self.reactorlist = [] # list of objects expecting to pool keyboard state when they update
        self.fps_display = pyglet.clock.ClockDisplay()

        self.renderlist.append(playership)
        self.renderlist.append(self.fps_display)
        self.reactorlist.append(playership)

        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def connect(self, control):
        """Respond to the connecting controller.

        :Parameters:
            `control` : Controller
                The connecting Controller object.

        """
        super(LevelBase, self).connect(control)
        playership.SetWindowHeight(self.window.height)

    def on_draw(self):
        self.window.clear()
        for drawable in self.renderlist:
            drawable.draw()

    def update(self, dt):
        if self.window is None:
            return
        for actor in self.actorlist:
            actor.Tick(dt)
        for reactor in self.reactorlist:
            reactor.Tick(dt, self.keys)

        ## Hacks
        for rock in rocks:
            rock["x"] = rock["x"] - ((dt/SECONDS_TO_CROSS_SCREEN)* self.window.width)
            if rock["x"] < 0:
                rocks.remove(rock)
        rockprob = random.randrange(100)
        if (rockprob > 95) and (len(rocks) < 5):
            rocks.append({"x":self.window.width, "y":random.randrange(self.window.height)})
            
        e_ship_prob = random.randrange(100)
        if(e_ship_prob > 98):
            x = self.window.width
            y = random.randrange(self.window.height)
            e_ship = entities.HostileShip(x, y, self)

            
    def remove_entity(self, entity):
        if entity in self.actorlist:
            self.actorlist.remove(entity)
        if entity in self.reactorlist:
            self.reactorlist.remove(entity)
        if entity in self.renderlist:
            self.renderlist.remove(entity)

class LevelOne(LevelBase):
    '''
    Level One
    '''
    name = "level1"

    def __init__(self ):
        super(LevelOne, self).__init__()
        self.level_label = pyglet.text.Label("Level One", font_size=20)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

        for rock in rocks:
            rock_label.x = rock["x"]
            rock_label.y = rock["y"]
            rock_label.draw()
    
    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("level2")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

class LevelTwo(LevelBase):
    '''
    Level Two
    '''
    name = "level2"

    def __init__(self ):
        super(LevelTwo, self).__init__()
        self.level_label = pyglet.text.Label("Level Two", font_size=20)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

        for rock in rocks:
            rock_label.x = rock["x"]
            rock_label.y = rock["y"]
            rock_label.draw()
    
    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("level1")
        else:
            return EVENT_UNHANDLED

