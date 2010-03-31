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
import data

SECONDS_TO_CROSS_SCREEN = 8

rocks = []

class Titlescreen(mode.Mode):
    '''
    The title screen manager. Derives from Mode.
    '''
    name = "titlescreen"
    def __init__(self):
        mode.Mode.__init__(self)

        self._Sprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/TitleScreenWS.jpg')))

    def connect(self, control):
        mode.Mode.connect(self, control)
        self._Sprite.image.width = self.window.width
        self._Sprite.image.height = self.window.height

    def update(self, dt):
        mode.Mode.update(self, dt)

    def on_draw(self):
        self._Sprite.draw()

    def on_key_press(self, sym, mods):
        if sym == key.ENTER:
            self.control.switch_handler("level1")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

class FullscreenScrollingSprite(gamestate.Actor):
    '''
    A class to manage a full-screen scrolling sprite.
    '''
    def __init__(self, filename, parent_level):
        self.Sprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath(filename)))
        gamestate.Actor.__init__(self, parent_level)
        self._ParallaxEffect = .7
        self.Sprite.opacity = 128

    def SetWindowHeight(self, window_height):
        assert(window_height != 0)
        assert(self.Sprite.height != 0)
        self.Sprite.scale = float(window_height) / float(self.Sprite.height)
        gamestate.Actor.SetWindowHeight(self, window_height)

    def Tick(self, dt):
        self.Sprite.x -= (self._WindowWidth * (dt / SECONDS_TO_CROSS_SCREEN)) * self._ParallaxEffect
        if (self.Sprite.x < -self.Sprite.width):
            self.Sprite.x += self.Sprite.width

        gamestate.Actor.Tick(self, dt)

    def draw(self):
        original_x = self.Sprite.x
        while (self.Sprite.x + self.Sprite.width < self._WindowWidth + self.Sprite.width):
            self.Sprite.draw()
            self.Sprite.x += self.Sprite.width
        self.Sprite.x = original_x

        gamestate.Actor.draw(self)

class LevelBase(mode.Mode):
    '''
    A base class for game levels
    '''
    name = "levelbase"
    def __init__(self):
        '''
        Create a level that runs in the given window
        '''
        super(LevelBase, self).__init__()
        self.window = None
        self.renderlist = []
        self.actorlist = []
        self.reactorlist = [] # list of objects expecting to pool keyboard state when they update

        self.fps_display = pyglet.clock.ClockDisplay()

    def connect(self, control):
        """Respond to the connecting controller.

        :Parameters:
            `control` : Controller
                The connecting Controller object.

        """
        super(LevelBase, self).connect(control)
        for drawable in self.renderlist:
            drawable.SetWindowHeight(self.window.height)
            drawable.SetWindowWidth(self.window.width)

    def on_draw(self):
        self.window.clear()
        for drawable in self.renderlist:
            drawable.draw()
        self.fps_display.draw()

    def update(self, dt):
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

    def get_width(self):
        if self.window is None:
            return 640
        return self.window.width

    def get_height(self):
        if self.window is None:
            return 480
        return self.window.height

    def remove_entity(self, entity):
        if entity in self.actorlist:
            self.actorlist.remove(entity)
        if entity in self.reactorlist:
            self.reactorlist.remove(entity)
        if entity in self.renderlist:
            self.renderlist.remove(entity)

    def register_entity(self, entity, entity_flag):
        if(entity_flag is ENTITY_STATIC):
            self.renderlist.append(entity)
        elif(entity_flag is ENTITY_ACTOR):
            self.renderlist.append(entity)
            self.actorlist.append(entity)
        elif(entity_flag is ENTITY_REACTOR):
            self.renderlist.append(entity)
            self.reactorlist.append(entity)

class LevelOne(LevelBase):
    '''
    Level One
    '''
    name = "level1"

    def __init__(self ):
        super(LevelOne, self).__init__()

        self.level_label = pyglet.text.Label("Level One", font_size=20)
        self.playership = player.Player(self)
        self.Background = FullscreenScrollingSprite('graphics/Level1Background.png', self)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

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
        self.playership = player.Player(self)
        self.Background = FullscreenScrollingSprite('graphics/Level2Background.png', self)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("level1")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED
