'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode
from entities import *
import config
from common import *
from constants import *
import pyglet
from pyglet.window import key

import random
import player
import entities
import data

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
    #    self.window.push_handlers(on_resize = self.on_resize)
    #
    # def disconnect (self, control):
    #    mode.Mode.disconnect(self, control)
    #    self.window.remove_handlers(self.on_resize)

    def on_resize(self, width, height):
        self._Sprite.image.width = self.window.width
        self._Sprite.image.height = self.window.height

    def update(self, dt):
        mode.Mode.update(self, dt)

    def on_draw(self):
        #self.window.clear()
        self._Sprite.draw()

    def on_key_press(self, sym, mods):
        if sym == key.ENTER:
            self.control.switch_handler("level2")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

class FullscreenScrollingSprite(Actor):
    '''
    A class to manage a full-screen scrolling sprite.
    '''
    def __init__(self, filename, parent_level, layer = 2, scrolling_factor = 1.0):
        self.Sprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath(filename)))
        Actor.__init__(self, parent_level, layer=layer)
        self._x = 0
        self._y = 0
        self._ParallaxEffect = .8
        self.Sprite.opacity = 255
        self._scrolling_factor = scrolling_factor

    def Rescale(self, NewScaleFactor):
        Actor.Rescale(self, NewScaleFactor)
        self.Sprite.scale = float(NewScaleFactor) * (float(SIZE_OF_GAMESPACE_Y) / float(self.Sprite.image.height))

    def Tick(self, dt):
        self._x -= (SIZE_OF_GAMESPACE_X * (dt / SECONDS_TO_CROSS_GAMESPACE)) * self._ParallaxEffect * self._scrolling_factor
        if (self._x < -self.Sprite.image.width):
            self._x += self.Sprite.image.width

        Actor.Tick(self, dt)

    def draw(self):
        x = self._x
        while (x + self.Sprite.image.width < SIZE_OF_GAMESPACE_X + self.Sprite.image.width):
            self.Sprite.x = int(self.GetScaledX(x) - .5)
            self.Sprite.y = int(self.GetScaledY(self._y) - .5)
            self.Sprite.draw()
            x += self.Sprite.image.width

        Actor.draw(self)

    def get_hitbox(self):
        # TODO: make this hit box smaller
        return (self.Sprite.x, self.Sprite.y, self.Sprite.width, self.Sprite.height)

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
        self.renderlist_layers = [[],[],[],[],[]]
        self.actorlist = []
        self.reactorlist = [] # list of objects expecting to pool keyboard state when they update

        self._scale = 1
        self._x_offset = 0
        self._y_offset = 0

        self.letterbox_1 = None
        self.letterbox_2 = None

        self.fps_display = pyglet.clock.ClockDisplay()

        
    def on_resize(self, width, height):
        self.Rescale()

    def Rescale(self):
        if self.window is None:
            return
        window_x = self.window.width
        window_y = self.window.height

        x_scale = float(window_x)/float(SIZE_OF_GAMESPACE_X)
        y_scale = float(window_y)/float(SIZE_OF_GAMESPACE_Y)

        if y_scale < x_scale:
            self._scale = y_scale
            self._y_offset = 0
            self._x_offset = int((float(window_x) - float(SIZE_OF_GAMESPACE_X) * self._scale)/2 + .5)
        else:
            self._scale = x_scale
            self._x_offset = 0
            self._y_offset = int((float(window_y) - float(SIZE_OF_GAMESPACE_Y) * self._scale)/2 + .5)

        for renderlist in self.renderlist_layers:
            for drawable in renderlist:
                drawable.Rescale(self._scale)
                drawable.SetOffsets(self._x_offset, self._y_offset)

        if self._x_offset != 0:
            letterbox = pyglet.image.SolidColorImagePattern((0, 0, 0, 255))
            letterbox_image = pyglet.image.create(int(self._x_offset ), self.window.height, letterbox)
            self.letterbox_1 = pyglet.sprite.Sprite(letterbox_image, x=0, y=0)
            self.letterbox_2 = pyglet.sprite.Sprite(letterbox_image, x=self.window.width - self._x_offset, y=0)
        elif self._y_offset != 0:
            letterbox = pyglet.image.SolidColorImagePattern((0, 0, 0, 255))
            letterbox_image = pyglet.image.create(self.window.width, int(self._y_offset), letterbox)
            self.letterbox_1 = pyglet.sprite.Sprite(letterbox_image, x=0, y=0)
            self.letterbox_2 = pyglet.sprite.Sprite(letterbox_image, x=0, y=self.window.height - self._y_offset)
        else:
            self.letterbox_1 = None
            self.letterbox_2 = None

    def on_draw(self):
        self.window.clear()

        # see if any of the actors collided with the player.
        for a in self.actorlist:
            if(self.playership.CollidedWith(a)):
                break;

        for renderlist in self.renderlist_layers:
            for drawable in renderlist:
                drawable.draw()

        if self.letterbox_1 is not None:
            self.letterbox_1.draw()
        if self.letterbox_2 is not None:
            self.letterbox_2.draw()
        self.fps_display.draw()

    def update(self, dt):
        for actor in self.actorlist:
            actor.Tick(dt)
        for reactor in self.reactorlist:
            reactor.Tick(dt, self.keys)

        ## Hacks
        for rock in rocks:
            rock["x"] = rock["x"] - ((dt/SECONDS_TO_CROSS_GAMESPACE)* SIZE_OF_GAMESPACE_X)
            if rock["x"] < 0:
                rocks.remove(rock)
        rockprob = random.randrange(100)
        if (rockprob > 95) and (len(rocks) < 5):
            rocks.append({"x":SIZE_OF_GAMESPACE_X, "y":random.randrange(SIZE_OF_GAMESPACE_Y)})

        e_ship_prob = random.randrange(100)
        if(e_ship_prob > 90):
            x = SIZE_OF_GAMESPACE_X
            #y = random.randrange(SIZE_OF_GAMESPACE_Y)
            y = 359
            e_ship = entities.HostileShip(x, y, self)


    def remove_entity(self, entity):
        if entity in self.actorlist:
            self.actorlist.remove(entity)
        if entity in self.reactorlist:
            self.reactorlist.remove(entity)
        for renderlist in self.renderlist_layers:
            if entity in renderlist:
                renderlist.remove(entity)

    def register_entity(self, entity, entity_flag, layer = 2):

        entity.Rescale(self._scale)
        entity.SetOffsets(self._x_offset, self._y_offset)

        assert layer >= 0 and layer < 5, 'Invalid layer number (%i)' % layer
        self.renderlist_layers[layer].append(entity)

        def compare_depth(x,y):
            xz = 0 if not hasattr(x,'z') else x.z
            yz = 0 if not hasattr(y,'z') else y.z
            return 1 if xz>yz else -1 if xz<yz else 0
        self.renderlist_layers[layer].sort(cmp=compare_depth)

        if(entity_flag is ENTITY_STATIC):
            pass
        elif(entity_flag is ENTITY_ACTOR):
            self.actorlist.append(entity)
        elif(entity_flag is ENTITY_REACTOR):
            self.reactorlist.append(entity)


#===============================================================================
#
# class TimeLineEntity:
#    def __init__(self, constructor, parameter_list):
#        self._constructor = constructor
#        self._parameter_list = parameter_list
#        self._object = None
#
#    def realize(self):
#        self._object = self._constructor(*(self._parameter_list))
#        return self._objec
#
#    def get_object(self):
#        if (self._object == None):
#            return self.realize()
#        retirm self._object
#
# class TimeLine:
#    def __init__(self, parent_level):
#        self._parent_level = parent_level
#        self._current_time = 0
#
#        #Fixtures are entities that should always be realized
#        self._fixtures = [
#            TimeLineEntity(player.Player, [parent_level]),
#            TimeLineEntity(FullscreenScrollingSprite, ['graphics/Level1Background.png', parent_level])
#            ]
#
#        self._timeline = {
#            0.5:TimeLineEntity(entities.rock, [self.window.width, random.randrange(self.window.height]),
#
#            }
#
#    def
#
#        player.Player(self)
#        FullscreenScrollingSprite('graphics/Level1Background.png', self)
#===============================================================================


class LevelOne(LevelBase):
    '''
    Level One
    '''
    name = "level1"

    def __init__(self ):
        super(LevelOne, self).__init__()
        self.level_label = pyglet.text.Label("Level One", font_size=20)
        self.playership = player.Player(self)
        self._Background = FullscreenScrollingSprite('graphics/Level1Background.png', self, 0, 0.0)
    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
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
        self._Background = FullscreenScrollingSprite('graphics/Level1Background.png', self, 0, 0.0)
        #self._Middleground = FullscreenScrollingSprite('graphics/Level1Middleground.png', self, 0, 0.5)
        #self._Foreground = FullscreenScrollingSprite('graphics/Level1Foreground.png', self, 1, 1.0)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
            self.control.switch_handler("level1")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED
