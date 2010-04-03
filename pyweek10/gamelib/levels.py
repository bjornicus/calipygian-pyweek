'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''
import pyglet
from pyglet import media
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode
from entities import *
import config
from common import *
from constants import *
from collide import *

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
        self.select_arrow = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/SelectionArrowBlue.png')))
        self.select_arrow.image.anchor_x = self.select_arrow.image.width
        self.select_arrow.image.anchor_y = self.select_arrow.image.height/2
        self.select_arrow.scale = 0.25
        self.selected_option = 'start'
        self.music_player = media.Player()
        self.music = data.load_song('TitlescreenMusic.ogg')

    def on_resize(self, width, height):
        if self.window is None:
            return
        window_x = self.window.width
        window_y = self.window.height

        x_scale = float(window_x)/float(self._Sprite.image.width)
        y_scale = float(window_y)/float(self._Sprite.image.height)

        if y_scale < x_scale:
            self._Sprite.scale = y_scale
            self._Sprite.y = 0
            self._Sprite.x =  int((float(window_x) - float(self._Sprite.image.width) * y_scale)/2 + .5)
        else:
            self._Sprite.scale = x_scale
            self._Sprite.x =  0
            self._Sprite.y = int((float(window_y) - float(self._Sprite.image.height) * x_scale)/2 + .5)

    def connect(self, control):
        super(Titlescreen, self).connect(control)
        
        if self.music is not None:
            self.music_player.queue(self.music)
            self.music_player.play()

    def disconnect(self):
        super(Titlescreen, self).disconnect()
        self.music_player.pause()

    def update(self, dt):
        mode.Mode.update(self, dt)

    def on_draw(self):
        self._Sprite.draw()
        if self.selected_option == 'start':
            self.select_arrow.position = (400, 250)
            self.select_arrow.draw()
        elif self.selected_option == 'quit':
            self.select_arrow.position = (400, 200)
            self.select_arrow.draw()

    def on_key_press(self, sym, mods):
        if sym == key.UP or sym == key.DOWN:
            self.selected_option = 'start' if self.selected_option == 'quit' else 'quit'
        elif sym == key.ENTER:
            if self.selected_option == 'start':
                self.control.switch_handler("level1")
            elif self.selected_option == 'quit':
                self.window.dispatch_event('on_close')
            else:
                return EVENT_UNHANDLED
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

class FullscreenScrollingSprite(Entity):
    '''
    A class to manage a full-screen scrolling sprite.
    '''
    def __init__(self, filename, parent_level, layer = 2, scrolling_factor = 1.0):
        self.Image = pyglet.image.load(data.filepath(filename))
        self._ImagePieces = []
        x = 0
        while x < self.Image.width:
            width = min(SIZE_OF_GAMESPACE_X, self.Image.width - x)
            self._ImagePieces.append(self.Image.get_region(x, 0, width, self.Image.height))
            x += width

        Entity.__init__(self, parent_level, layer=layer)
        self._x = 0
        self._y = 0
        self._scrolling_factor = scrolling_factor

    def Rescale(self, NewScaleFactor):
        super(FullscreenScrollingSprite, self).Rescale(NewScaleFactor)
        self._scale = float(NewScaleFactor) * (float(SIZE_OF_GAMESPACE_Y) / float(self.Image.height))

    def Tick(self, dt):
        self._x -= (SIZE_OF_GAMESPACE_X * (dt / SECONDS_TO_CROSS_GAMESPACE)) * self._scrolling_factor
        if (self._x < -self.Image.width):
            self._x += self.Image.width

        super(FullscreenScrollingSprite, self).Tick(dt)

    def draw(self):
        x = int(self._x - 0.5)
        while (x + self.Image.width < SIZE_OF_GAMESPACE_X + self.Image.width):
            x_offset = x
            for image in self._ImagePieces:
                if (x_offset + image.width < 0 or x_offset > SIZE_OF_GAMESPACE_X):
                    pass
                else:
                    image.blit(self.GetScaledX(x_offset), 0)
                x_offset += image.width

            x += self.Image.width

        super(FullscreenScrollingSprite, self).draw()


    def get_collidable(self):
        return None

class LevelBase(mode.Mode):
    '''
    A base class for game levels
    '''
    name = "levelbase"
    def __init__(self):
        '''
        Create a level that runs in the given window
        '''
        mode.Mode.__init__(self)
        self.window = None
        self.renderlist_layers = [[],[],[],[],[]]
        self.actorlist = []

        self._scale = 1
        self._x_offset = 0
        self._y_offset = 0

        self.letterbox_1 = None
        self.letterbox_2 = None

        self.fps_display = pyglet.clock.ClockDisplay()
        self.music_player = media.Player()
        self.music = None
        self.player = player.Player(self)
        
    def connect(self, control):
        mode.Mode.connect(self, control)
        
        # Immedietly rescale the gamefield to the window
        self.Rescale()
        if self.music is not None:
            self.music_player.queue(self.music)
            self.music_player.play()

    def disconnect(self):
        super(LevelBase, self).disconnect()
        self.music_player.pause()
        
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

        for renderlist in self.renderlist_layers:
            for drawable in renderlist:
                drawable.draw()

        if self.letterbox_1 is not None:
            self.letterbox_1.draw()
        if self.letterbox_2 is not None:
            self.letterbox_2.draw()
        self.fps_display.draw()

    def update(self, dt):
        self.player.handle_input(self.keys)
        for actor in self.actorlist:
            actor.Tick(dt)
        self.player.reset_color()
        # see if any of the actors collided with the player.
        for a in self.actorlist:
            if(collide(self.player.get_collidable(), a.get_collidable())):
                self.player.on_collision();
                break;

    def on_key_press(self, sym, mods):
        if sym == key.ESCAPE:
            self.control.switch_handler("titlescreen")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def remove_entity(self, entity):
        if entity in self.actorlist:
            self.actorlist.remove(entity)
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

        if(isinstance(entity, Actor)):
            self.actorlist.append(entity)


class TimeLineEntity:
    """
    Class for storing the locations of entities that will appear within a level
    
    Entities are not initialized until the realize method is called, at which
    point their constructor is called along with the provided list of parameters
    (parameters will be given to the constructor in the order they are provided)
    or keywords (keywords must be provided in a dictionary of keyword:value mappings.
    """
    def __init__(self, constructor, parameter_list = [], keywords_list = {}):
        self._constructor = constructor
        self._parameter_list = parameter_list
        self._keywords_list = keywords_list
        self._object = None

    def realize(self):
        self._object = self._constructor(*(self._parameter_list), **(self._keywords_list))
        return self._object

    def get_object(self):
        return self._object

class TimeLine:
    """
    Class for storing the sequence of entities that will appear within a level
    
    A dictionary of time:TimeLineEntity mappings is provided to the constructor.
    
    Every tick we check to see if any of the times listed in the keys of the provided
    timeline has passed, if so we call realize on the corresponding TimeLineEntity, and
    call tick on the resultant object in order to make up for any imprecision in the update
    loop.
    """
    def __init__(self, timeline):
        assert(timeline is not None)
        self._current_time = 0
        self._timeline = timeline
        self._event_times = self._timeline.keys()

        self._event_times.sort()
        self._event_times.reverse()

    def Tick(self, dt):
        tick_end = self._current_time + dt
        while len(self._event_times) > 0 :
            event_time = self._event_times.pop()
            if event_time <= tick_end:
                self._timeline[event_time].realize()
                self._timeline[event_time].get_object().Tick(tick_end - event_time)
            else:
                self._event_times.append(event_time)
                break
        self._current_time = tick_end


class LevelOne(LevelBase):
    '''
    Level One
    '''
    name = "level1"

    def __init__(self ):
        LevelBase.__init__(self)
        self.level_label = pyglet.text.Label("Level One", font_size=20)
        self._Background = FullscreenScrollingSprite('graphics/Level1Background.png', self, 0, 0.0)
        self._Middleground = FullscreenScrollingSprite('graphics/Level1Middleground.png', self, 0, 0.25)
        self._Foreground = FullscreenScrollingSprite('graphics/Level1Foreground.png', self, 1, 1.0)
        self.music = data.load_song('Level1Music.ogg')

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
            self.control.switch_handler("level2")
        else:
            return LevelBase.on_key_press(self, sym, mods)
        return EVENT_HANDLED

class LevelTwo(LevelBase):
    '''
    Level Two
    '''
    name = "level2"

    def __init__(self ):
        LevelBase.__init__(self)
        self.level_label = pyglet.text.Label("Level Two", font_size=20)
        self._Background = FullscreenScrollingSprite('graphics/Level2Background.png', self, 0, 0.0)
        self._Middleground = FullscreenScrollingSprite('graphics/Level2Middleground.png', self, 0, 0.25)
        self._Foreground = FullscreenScrollingSprite('graphics/Level2Foreground.png', self, 1, 1.0)
        self.music = data.load_song('Level2Music.ogg')

        self._timeline = TimeLine({
            2:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, self]),
            6:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 300, self]),
            12:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 200, self]),
            12.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 190, self]),
            12.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 180, self]),
            12.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 170, self]),
            15:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 400, self])
            })

    def update(self, dt):
        self._timeline.Tick(dt)
        LevelBase.update(self, dt)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
            self.control.switch_handler("level3")
        else:
            return LevelBase.on_key_press(self, sym, mods)
        return EVENT_HANDLED


class LevelThree(LevelBase):
    '''
    Level Three
    '''
    name = "level3"

    def __init__(self ):
        LevelBase.__init__(self)
        self.level_label = pyglet.text.Label("Level Three", font_size=20)
        self._Background = FullscreenScrollingSprite('graphics/Level3Background.png', self, 0, 0.0)
        self._Middleground = FullscreenScrollingSprite('graphics/Level3Middleground.png', self, 0, 0.25)
        self._Foreground = FullscreenScrollingSprite('graphics/Level3Foreground.png', self, 1, 1.0)
        self.music = data.load_song('Level3Music.ogg')

        self._timeline = TimeLine({
            2:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, self]),
            6:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 300, self]),
            12:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 200, self]),
            12.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 190, self]),
            12.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 180, self]),
            12.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 170, self]),
            15:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 400, self])
            })

    def update(self, dt):
        self._timeline.Tick(dt)
        LevelBase.update(self, dt)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
            self.control.switch_handler("level4")
        else:
            return LevelBase.on_key_press(self, sym, mods)
        return EVENT_HANDLED


class LevelFour(LevelBase):
    '''
    Level Four
    '''
    name = "level4"

    def __init__(self ):
        LevelBase.__init__(self)
        self.level_label = pyglet.text.Label("Level Four", font_size=20)
        self._Background = FullscreenScrollingSprite('graphics/Level4Background.png', self, 0, 0.0)
        self._Middleground = FullscreenScrollingSprite('graphics/Level4Middleground.png', self, 0, 0.25)
        self._Foreground = FullscreenScrollingSprite('graphics/Level4Foreground.png', self, 1, 1.0)
        self.music = data.load_song('Level4Music.ogg')

        self._timeline = TimeLine({
            2:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, self]),
            6:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 300, self]),
            12:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 200, self]),
            12.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 190, self]),
            12.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 180, self]),
            12.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 170, self]),
            15:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 400, self])
            })
                
    def update(self, dt):
        self._timeline.Tick(dt)
        LevelBase.update(self, dt)

    def on_draw(self):
        LevelBase.on_draw(self)
        self.level_label.draw()

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
            self.control.switch_handler("level1")
        else:
            return LevelBase.on_key_press(self, sym, mods)
        return EVENT_HANDLED


