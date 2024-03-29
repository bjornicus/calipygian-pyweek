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
from constants import *

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
import entities
import gamelib.entities

if DEBUG:
    from debug import *



NEXT_LEVEL = 'level1'
def set_next_level(name):
    global NEXT_LEVEL
    NEXT_LEVEL = name

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
        self.music = None
        self.music = data.load_song('TitlescreenMusic.ogg')

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
                self.control.switch_handler('levelselect')
            elif self.selected_option == 'quit':
                self.window.dispatch_event('on_close')
            else:
                return EVENT_UNHANDLED
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

class LevelSelect(mode.Mode):
    '''
    The level selection screen. Derives from Mode.
    '''
    name = "levelselect"
    def __init__(self):
        mode.Mode.__init__(self)

        self._Sprite = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/LevelSelectWS.jpg')))
        self.select_arrow = pyglet.sprite.Sprite(pyglet.image.load(data.filepath('graphics/SelectionArrowBlue.png')))
        self.select_arrow.image.anchor_x = self.select_arrow.image.width/2
        self.select_arrow.image.anchor_y = self.select_arrow.image.height/2
        self.select_arrow.scale = 0.75
        self.selected_option = 0
        self.music_player = media.Player()
        self.music = None
        self.music = data.load_song('LevelSelectMusic.ogg')
        self.select_arrow_positions = [(526, 480-67), (526, 480-173), (526, 480-278), (526, 480-387)]

    def connect(self, control):
        super(LevelSelect, self).connect(control)

        if self.music is not None:
            self.music_player.queue(self.music)
            self.music_player.play()

    def disconnect(self):
        super(LevelSelect, self).disconnect()
        self.music_player.pause()

    def update(self, dt):
        mode.Mode.update(self, dt)

    def on_draw(self):
        self._Sprite.draw()
        self.select_arrow.position = self.select_arrow_positions[self.selected_option]
        self.select_arrow.draw()

    def on_key_press(self, sym, mods):
        if sym == key.UP:
            self.selected_option -= 1
            set_next_level('level' + str(self.selected_option+1))
            if self.selected_option < 0:
                self.selected_option = 3
        elif sym == key.DOWN:
            self.selected_option += 1
            set_next_level('level' + str(self.selected_option+1))
            if self.selected_option > 3:
                self.selected_option = 0
        elif sym == key.ESCAPE:
            self.control.switch_handler("titlescreen")
        elif sym == key.ENTER:
            self.control.switch_handler("loading")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

class Loading(mode.Mode):
    '''
    The loading screen. Derives from Mode.
    '''
    name = "loading"
    def __init__(self):
        mode.Mode.__init__(self)
        filename = data.filepath('graphics/Loading.png')
        if (NEXT_LEVEL == 'level1'):
            filename = data.filepath('graphics/Level1Story.jpg')
        if (NEXT_LEVEL == 'level2'):
            filename = data.filepath('graphics/Level2Story.jpg')
        elif (NEXT_LEVEL == 'level3'):
            filename = data.filepath('graphics/Level3Story.jpg')
        elif (NEXT_LEVEL == 'level4'):
            filename = data.filepath('graphics/Level4Story.jpg')
        self._Background = pyglet.sprite.Sprite(pyglet.image.load(filename))
        self._Connected = False
        self._Frames = 0

    def connect(self, control):
        super(Loading, self).connect(control)
        self._Connected = True

    def disconnect(self):
        super(Loading, self).disconnect()

    def update(self, dt):
        mode.Mode.update(self, dt)

    def on_draw(self):
        self._Frames += 1
        self._Background.draw()
        if self._Connected and self._Frames > 10:
            self.control.switch_handler(NEXT_LEVEL)

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
        self._objects_of_interest = {}
        self._Background = None
        self._Middleground = None
        self._Foreground = None

        self._letterbox_1 = None
        self._letterbox_2 = None

        self.fps_display = pyglet.clock.ClockDisplay()
        self.music_player = media.Player()
        self.music = None

        self.timeline = TimeLine({})
        self.endtime = DEFAULT_LEVEL_TIME

        thePlayer = player.Player(self)
        player.Hud(self,thePlayer)

        self.LevelTimeScale = 1.0
        self.ChangeSplash('LevelStartReady.png')

        # construction and loading of levels can take quite a while, the result is
        # that the first time update gets called, the dt is quite large
        # this causes strangeness, so we ignore the first update.
        # once update gets called it should start ticking along nicely
        self.ignore_next_update = True

    def connect(self, control):
        mode.Mode.connect(self, control)

        if self.music is not None:
            self.music_player.queue(self.music)
            self.music_player.play()
        pyglet.clock.schedule_once(self.on_level_complete, self.endtime)
        self.restart()

    def disconnect(self):
        super(LevelBase, self).disconnect()
        self.music_player.pause()
        pyglet.clock.unschedule(self.on_level_complete)

    def setup_timeline(self):
        pass

    def restart(self):
        pyglet.clock.unschedule(self.on_level_complete)
        self.renderlist_layers = [[],[],[],[],[]]
        self.actorlist = []
        self._objects_of_interest = {}
        thePlayer = player.Player(self)
        player.Hud(self, thePlayer)
        if self._Background:
            self.register_entity(self._Background, 0)
        if self._Middleground:
            self._Middleground.reset()
            self.register_entity(self._Middleground, 0)
        if self._Foreground:
            self._Foreground.reset()
            self.register_entity(self._Foreground, 1, TYPE_TERRAIN)

        self.setup_timeline()
        pyglet.clock.schedule_once(self.on_level_complete, self.endtime)

    def on_level_complete(self, dt=0):
        self.ChangeSplash('LevelEndCongratulations.png')

    def on_draw(self):
        self.window.clear()

        for renderlist in self.renderlist_layers:
            for drawable in renderlist:
                drawable.draw()

        self.fps_display.draw()

        if self._ShowingSplash:
            self._SplashSprite.draw()

    def update(self, dt):
        dt *= self.LevelTimeScale
        if self.ignore_next_update:
            self.ignore_next_update = False
            return
        self.timeline.update(dt)
        for actor in self.actorlist:
            actor.update(dt)

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships:
            playership.handle_input(self.keys)
            playership.reset_color()
            # see if any of the actors collided with the player.
            playership_collider = playership.get_collidable()
            hostiles = self.get_objects_of_interest(TYPE_HOSTILE_SHIP)
            for baddie in hostiles:
                if collide(playership_collider, baddie.get_collidable()):
                    print "HIT"
                    playership.on_collision()
                    self.remove_entity(baddie)
            terrains = self.get_objects_of_interest(TYPE_TERRAIN)
            terrain_collision = False
            for terrain in terrains:
                if terrain.collide(playership_collider):
                    terrain_collision = True
            playership.hitting_terrain = terrain_collision

    def on_key_press(self, sym, mods):
        if DEBUG and sym == key.BACKSPACE:
            self.on_level_complete()
        elif sym == key.ESCAPE:
            self.control.switch_handler("titlescreen")
        elif self._ShowingSplash:
            self.ChangeSplash()
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def ChangeSplash(self, NewSplash = None):
        if NewSplash is None:
            self._ShowingSplash = False
            if (self._CurrentSplash == 'LevelStartReady.png'):
                self._CurrentSplash = 'LevelStartGo.png'
                self._ShowingSplash = True
            elif (self._CurrentSplash == 'LevelEndCongratulations.png'):
                self.control.switch_handler('loading')
            elif (self._CurrentSplash == 'ShipExploded.png'):
                self.restart()
        else:
            self._CurrentSplash = NewSplash
            self._ShowingSplash = True

        if (self._ShowingSplash):
            self.LevelTimeScale = 0.1
        else:
            self.LevelTimeScale = 1.0
        self._SplashSprite = pyglet.sprite.Sprite(data.load_image(self._CurrentSplash))
        self._SplashSprite.x = SIZE_OF_GAMESPACE_X / 2 - self._SplashSprite.width / 2
        self._SplashSprite.y = SIZE_OF_GAMESPACE_Y / 2 - self._SplashSprite.height / 2

    def remove_entity(self, entity, object_of_interest_type = None):
        if entity in self.actorlist:
            self.actorlist.remove(entity)
        for renderlist in self.renderlist_layers:
            if entity in renderlist:
                renderlist.remove(entity)

        if(object_of_interest_type is not None):
            if object_of_interest_type in self._objects_of_interest.keys():
                self._objects_of_interest[object_of_interest_type].remove(entity)

    def register_entity(self, entity, layer = 2, object_of_interest_type = None):
        assert layer >= 0 and layer < 5, 'Invalid layer number (%i)' % layer
        self.renderlist_layers[layer].append(entity)

        def compare_depth(x,y):
            xz = 0 if not hasattr(x,'z') else x.z
            yz = 0 if not hasattr(y,'z') else y.z
            return 1 if xz>yz else -1 if xz<yz else 0
        self.renderlist_layers[layer].sort(cmp=compare_depth)
        
        if(object_of_interest_type is not None):
            if object_of_interest_type in self._objects_of_interest.keys():
                self._objects_of_interest[object_of_interest_type].append(entity)
            else:
                self._objects_of_interest[object_of_interest_type] = [entity]

        self.actorlist.append(entity)
            
    def get_objects_of_interest(self, object_of_interest_type):
        if object_of_interest_type in self._objects_of_interest.keys():
            return self._objects_of_interest[object_of_interest_type]
        return []


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

    def update(self, dt):
        tick_end = self._current_time + dt
        while len(self._event_times) > 0 :
            event_time = self._event_times.pop()
            if event_time <= tick_end:
                self._timeline[event_time].realize()
                self._timeline[event_time].get_object().update(tick_end - event_time)
            else:
                self._event_times.append(event_time)
                break
        self._current_time = tick_end


class LevelZero(LevelBase):
    '''
    Level Zero
    '''
    name = "level0"

    def __init__( self ):
        print ''
        print 'Initializing Level Zero...'
        LevelBase.__init__(self)
        #self._Background = gamelib.entities.FullscreenScrollingSprite('graphics/Level0Background.png', self, 0, 0.0)
        #self._Middleground = gamelib.entities.FullscreenScrollingSprite('graphics/Level0Middleground.png', self, 0, 0.25*SHIP_SPEED)
        self._Foreground = entities.CollidableTerrain('graphics/Level0Foreground.png', self, 1, SHIP_SPEED)
        #self.music = data.load_song('Level1Music.ogg')

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships:
            playership.line_color = LEVEL1_PATH_COLOR
        self.setup_timeline()

    def setup_timeline(self):
         self.timeline = TimeLine({
            1:      TimeLineEntity(entities.TargetPath, [self,1]),
            5:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 50,  2,   self, 1]),
            })

    def connect(self, control):
        LevelBase.connect(self, control)
        set_next_level('level1')

class LevelOne(LevelBase):
    '''
    Level One
    '''
    name = "level1"

    def __init__( self ):
        print ''
        print 'Initializing Level One...'
        LevelBase.__init__(self)
        self._Background = gamelib.entities.FullscreenScrollingSprite('graphics/Level1Background.png', self, 0, 0.0)
        self._Middleground = gamelib.entities.FullscreenScrollingSprite('graphics/Level1Middleground.png', self, 0, 0.25*SHIP_SPEED)
        self._Foreground = entities.CollidableTerrain('graphics/Level1Foreground.png', self, 1, SHIP_SPEED)
        self.music = data.load_song('Level1Music.ogg')

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships:
            playership.line_color = LEVEL1_PATH_COLOR
        self.setup_timeline()

    def setup_timeline(self):
         self.timeline = TimeLine({
            1:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, 2,   self, 1]),
            5:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 50,  2,   self, 1]),
            15:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 400, 2,   self, 1]),
            17:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 50,  2,   self, 1]),
            23:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 300, 1.5, self, 2]),
            23.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 310, 1.5, self, 2]),
            23.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 320, 1.5, self, 2]),
            23.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 330, 1.5, self, 2]),
            30:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 40,  2,   self, 1]),
            35:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 1.5, self, 2]),
            40:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 320, 1.5, self, 2]),
            40.001: TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 160, 1.5, self, 2]),
            47:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 440, 2,   self, 1]),
            55:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 20,  1.5, self, 2]),
            55.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 30,  1.5, self, 2]),
            60:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 1.5, self, 2]),
            65:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 340, 1.5, self, 2]),
            65.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 330, 1.5, self, 2]),
            65.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 320, 1.5, self, 2]),
            65.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 310, 1.5, self, 2]),
            69:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 150, 2,   self, 1]),
            73:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, 2,   self, 1]),
            76:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 150, 2,   self, 1]),
            76.001: TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, 2,   self, 1]),
            81:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 150, 1.5, self, 2]),
            81.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, 1.5, self, 2]),
            81.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 170, 1.5, self, 2]),
            81.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 330, 1.5, self, 2]),
            82:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 190, 1.5, self, 2]),
            82.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 310, 1.5, self, 2]),
            85:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 4,   self, 3]),
            })


    def connect(self, control):
        LevelBase.connect(self, control)
        set_next_level('level2')



class LevelTwo(LevelBase):
    '''
    Level Two
    '''
    name = "level2"

    def __init__(self ):
        print ''
        print 'Initializing Level Two...'
        LevelBase.__init__(self)
        self._Background = gamelib.entities.FullscreenScrollingSprite('graphics/Level2Background.png', self, 0, 0.0)
        self._Middleground = gamelib.entities.FullscreenScrollingSprite('graphics/Level2Middleground.png', self, 0, 0.25*SHIP_SPEED)
        self._Foreground = entities.CollidableTerrain('graphics/Level2Foreground.png', self, 1, SHIP_SPEED)
        self.music = data.load_song('Level2Music.ogg')

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships: 
            playership.line_color = LEVEL2_PATH_COLOR
        self.setup_timeline()
                
    def setup_timeline(self):
         self.timeline = TimeLine({
            1:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 2,   self, 1]),
            5:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 1,   self, 2]),
            11:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 4,   self, 3]),
            17:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 3,   self, 4]),
            23:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 1,   self, 1]),
            30:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 2,   self, 2]),
            36:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 4,   self, 3]),
            42:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 3,   self, 4]),
            48:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 1,   self, 1]),
            54:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 2,   self, 2]),
            60:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 4,   self, 3]),
            66:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 3,   self, 4]),
            72:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 240, 1,   self, 1]),
            78:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 2,   self, 2]),
            84:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 3,   self, 4]),
            })


    def connect(self, control):
        LevelBase.connect(self, control)
        set_next_level('level3')


class LevelThree(LevelBase):
    '''
    Level Three
    '''
    name = "level3"

    def __init__(self ):
        print ''
        print 'Initializing Level Three...'
        LevelBase.__init__(self)
        self._Background = gamelib.entities.FullscreenScrollingSprite('graphics/Level3Background.png', self, 0, 0.0)
        self._Middleground = gamelib.entities.FullscreenScrollingSprite('graphics/Level3Middleground.png', self, 0, 0.25*SHIP_SPEED)
        self._Foreground = entities.CollidableTerrain('graphics/Level3Foreground.png', self, 1, SHIP_SPEED)
        self.music = data.load_song('Level3Music.ogg')

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships:
            playership.line_color = LEVEL3_PATH_COLOR
        self.setup_timeline()

    def setup_timeline(self):
         self.timeline = TimeLine({
            1:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 2,   self, 2]),
            11:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 210, 4,   self, 1]),
            21:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 1,   self, 3]),
            16:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 4,   self, 2]),
            48:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 210, 1,   self, 3]),
            60:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 4,   self, 1]),
            72:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 1,   self, 2]),
            84:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 210, 1,   self, 4]),
            })


    def connect(self, control):
        LevelBase.connect(self, control)
        set_next_level('level4')


class LevelFour(LevelBase):
    '''
    Level Four
    '''
    name = "level4"

    def __init__(self ):
        print ''
        print 'Initializing Level Four...'
        LevelBase.__init__(self)
        self._Background = gamelib.entities.FullscreenScrollingSprite('graphics/Level4Background.png', self, 0, 0.0)
        self._Middleground = gamelib.entities.FullscreenScrollingSprite('graphics/Level4Middleground.png', self, 0, 0.25*SHIP_SPEED)
        self._Foreground = entities.CollidableTerrain('graphics/Level4Foreground.png', self, 1, SHIP_SPEED)
        self.music = data.load_song('Level4Music.ogg')

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships: 
            playership.line_color = LEVEL4_PATH_COLOR
        self.setup_timeline()
                  
    def setup_timeline(self):
         self.timeline = TimeLine({
            1:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 2,   self, 2]),
            11:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 210, 4,   self, 1]),
            21:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 1,   self, 3]),
            16:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 4,   self, 2]),
            48:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 210, 1,   self, 3]),
            60:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 230, 4,   self, 1]),
            72:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 250, 1,   self, 2]),
            84:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 210, 1,   self, 4]),
            })

              
    def connect(self, control):
        LevelBase.connect(self, control)
        set_next_level('titlescreen')


class TestLevel(LevelBase):
    '''
    A small test level
    '''
    name = "testlevel"

    def __init__(self ):
        print ''
        print 'Initializing Test Level...'
        LevelBase.__init__(self)
        self.level_label = pyglet.text.Label("TEST LEVEL", font_size=20)
        #self._Background = FullscreenScrollingSprite('graphics/Level4Background.png', self, 0, 0.0)
        #self._Middleground = FullscreenScrollingSprite('graphics/Level4Middleground.png', self, 0, 0.25*SHIP_SPEED)
        self._Foreground = entities.CollidableTerrain('graphics/TestLevelForeground.png', self, 1, SHIP_SPEED)
        #self.music = data.load_song('Level4Music.ogg')

        playerships = self.get_objects_of_interest(TYPE_PLAYER_SHIP)
        for playership in playerships: 
            playership.line_color = LEVEL1_PATH_COLOR

        self.setup_timeline()
        self.endtime = 30
                
    def setup_timeline(self):         
        self.timeline = TimeLine({
            1:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 350, 2,   self, 1]),
            5:      TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 50,  2,   self, 1]),
            15:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 400, 2,   self, 1]),
            17:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 50,  2,   self, 1]),
            23:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 300, 1.5, self, 2]),
            23.25:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 310, 1.5, self, 2]),
            23.5:   TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 320, 1.5, self, 2]),
            23.75:  TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 330, 1.5, self, 2]),
            30:     TimeLineEntity(entities.HostileShip, [SIZE_OF_GAMESPACE_X, 40,  2,   self, 1]),
            })

    def connect(self, control):
        LevelBase.connect(self, control)
        set_next_level('level0')

