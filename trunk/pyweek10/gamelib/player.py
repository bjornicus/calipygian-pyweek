'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''
import pyglet
from pyglet.window import key
from pyglet.gl import *
import joystick
from entities import *
from constants import *
import config
import levels
import data
import math
from numpy import arange
import oscillator
if DEBUG:
    from debug import *

class Hud(Entity):
    entity_type = None
    SHIELD_BAR_WIDTH = 40
    SHIELD_BAR_MAX_LENGTH = 200
    def __init__(self, parent_level, player):
        self.x = 0
        self.y = SIZE_OF_GAMESPACE_Y - 10
        self._scale = 1
        self.player = player
        Entity.__init__(self, parent_level)

    def draw(self):
        percent_shield = self.player.shield/MAX_SHIELDS
        glLineWidth(Hud.SHIELD_BAR_WIDTH)
        glColor4f(1-percent_shield, percent_shield, 0, 0.8)
        glRectf(self.x, self.y, self.x + percent_shield * Hud.SHIELD_BAR_MAX_LENGTH ,self.y - Hud.SHIELD_BAR_WIDTH)
        glColor4f(1,1,1,1)
        glLineWidth(1)
        Entity.draw(self)
        

class Player(Actor, oscillator.Oscillator):
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator object.
    '''
    
    entity_type = TYPE_PLAYER_SHIP
    
    def __init__(self, parent_level):
        sprite_image = data.load_image('Ship.png')
        sprite_image.anchor_y = sprite_image.height/2
        Actor.__init__(self, sprite_image, parent_level)
        oscillator.Oscillator.__init__(self)
        self.x = PLAYER_OFFFSET_FROM_RIGHT_SCREEN_BOUND
        self.y = SIZE_OF_GAMESPACE_Y//2
        self.z = 1 #draw this above other stuff

        self._original_color = self.sprite.color
        self.line_color = (1, 0.5, 0, 0.9)
        self.shield = STARTING_SHIELDS
        self.collision_cooldown = 0
        self._hitting_terrain = False
        self.dpad = joystick.DPad()

    def getHudContents(self):
        timeleft = self.parent_level.endtime - self.parent_level.timeline._current_time
        return ["Shields:{0}".format(int(self.shield)),
                "Next Level In {0}".format(int(timeleft))]

    def Rescale(self, NewScaleFactor):
        super(Player, self).Rescale(NewScaleFactor)

    def update(self, dt):
        oscillator.Oscillator.update(self, dt)
        shipPos = self.GetCurrentValue()
        self.y  = SIZE_OF_GAMESPACE_Y//2 + (shipPos * SIZE_OF_GAMESPACE_Y//2)
        if self.hitting_terrain:
            self.shield -= SHIELD_TERRAIN_DRAIN_RATE
        self.shield = min(self.shield + SHIELD_CHARGE_RATE * dt * self._Omega,  MAX_SHIELDS)
        if self.shield < 0:
            self.die()
        if (self.collision_cooldown > 0):
            self.collision_cooldown = max(self.collision_cooldown - dt, 0)
        
    def handle_input(self, keys):
        self.dpad.update()
        if keys[key.UP] and not keys[key.DOWN] or self.dpad.axis1 < 0:
            self.AmplitudeAdjust = INCREASE
        elif keys[key.DOWN] and not keys[key.UP] or self.dpad.axis1 > 0:
            self.AmplitudeAdjust = DECREASE
        else:
            self.AmplitudeAdjust = CONSTANT

        if keys[key.LEFT] and not keys[key.RIGHT] or self.dpad.axis0 < 0:
            if config.reverse_frequency_keys:
                self.FrequencyAdjust = DECREASE
            else:
                self.FrequencyAdjust = INCREASE
        elif keys[key.RIGHT] and not keys[key.LEFT] or self.dpad.axis0 > 0:
            if config.reverse_frequency_keys:
                self.FrequencyAdjust = INCREASE
            else:
                self.FrequencyAdjust = DECREASE
        else:
            self.FrequencyAdjust = CONSTANT

        #=======================================================================
        # if keys[key.SPACE]:
        #    self.frozen = True
        # else: 
        #    self.frozen = False
        #=======================================================================


    def get_hitting_terrain(self):
        return self._hitting_terrain
    def set_hitting_terrain(self, hit):
        if not hit and self._hitting_terrain:
            self.on_terrain_depart()
        if hit and not self._hitting_terrain:
            self.on_terrain_contact()
        self._hitting_terrain = hit

    hitting_terrain = property(get_hitting_terrain, set_hitting_terrain)

    def on_terrain_contact(self):
        pass
    def on_terrain_depart(self):
        pass

    def reset_color(self):
        if self.hitting_terrain:
            self.sprite.color = (255,128,0)
        elif (self.collision_cooldown > 0):
            self.sprite.color = (255, 0, 0)
        else:
            self.sprite.color = self._original_color

    def on_collision(self):
        if (self.collision_cooldown > 0):
            return
        self.sprite.color = (255, 0, 0)
        self.shield -= 500
        self.collision_cooldown = COLLISION_COOLDOW

    def die(self):
        self.parent_level.ChangeSplash('ShipExploded.png')

    def get_collidable(self):
        return SpriteCollision(self.sprite)

    def draw(self):
        self.sprite.x = self.GetScaledX(self.x)
        self.sprite.y = self.GetScaledY(self.y)
        self.draw_path()
        Actor.draw(self)
        if DEBUG:
            draw_bounding_box(self.sprite)
        
    def draw_path(self):
        glColor4f(*self.line_color) 
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        for time in arange(0, SECONDS_TO_CROSS_GAMESPACE, 0.2/self._Omega):
            t, y, a = self.GetPredictiveCoordinate(time)
            x = self.GetScaledX(SIZE_OF_GAMESPACE_X * t/float(SECONDS_TO_CROSS_GAMESPACE) + self.x + self.sprite.width/2)
            y = self.GetScaledY(SIZE_OF_GAMESPACE_Y//2 + (y * SIZE_OF_GAMESPACE_Y//2))
            glVertex2f(x,y)
        glEnd()
        glLineWidth(1)
        glColor4f(1, 1, 1, 1) 

