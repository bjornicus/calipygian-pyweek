'''
Contains code for different levels of the game.
Levels render in a window, handle input, and update
the entities they contain.

'''

import pyglet
from pyglet.window import key
from pyglet.gl import *
from entities import *
from constants import *
import levels
import data
import math
from numpy import arange
if DEBUG:
    from debug import *

PATH_POINTS = 50.0

# hit box helpers.
HITBOX_X = lambda hitbox: hitbox[0]
HITBOX_Y = lambda hitbox: hitbox[1]
HITBOX_WIDTH = lambda hitbox: hitbox[2]
HITBOX_HEIGHT = lambda hitbox: hitbox[3]

class Hud(Entity):
    entity_type = None
    def __init__(self, parent_level):
        self.x = 0
        self.y = SIZE_OF_GAMESPACE_Y
        self._scale = 1
        
        self._lables = []
        self._hud_background = None
        
        Entity.__init__(self, parent_level)
        
    def ConstructHud(self, contents):
        
        max_x = 0
        y = 5
        self._lables = []    
        contents.reverse()
        for line in contents:
            label = pyglet.text.Label(line, font_size=20*self._scale) 
            max_x = max(max_x, label.content_width)
            self._lables.append((label, 0, y))
            y = y + label.content_height + 5
     
        hud_texture = pyglet.image.SolidColorImagePattern((0, 0, 0, 255))
        hud_image = pyglet.image.create(max_x, y, hud_texture)
        self._hud_background = pyglet.sprite.Sprite(hud_image)
        self._hud_background.image.anchor_y = self._hud_background.image.height
        self._hud_background.scale = float(self._scale)
        
    def Rescale(self, NewScaleFactor):
        Entity.Rescale(self, NewScaleFactor)
        self._scale = NewScaleFactor
        if self._hud_background is not None:
            self._hud_background.scale = float(NewScaleFactor)
        for label, x, y in self._lables:
            label.font_size = 20*self._scale
                    
    def Tick(self, delta_t):
        ships = self.parent_level.get_objects_of_interest(TYPE_PLAYER_SHIP)
        if len(ships) > 0:
            contents = ships[0].getHudContents()
            self.ConstructHud(contents)
        Entity.Tick(self, delta_t)
        
    def draw(self):
        Entity.draw(self)
        if self._hud_background is not None:
            self._hud_background.x = self.GetScaledX(self.x)
            self._hud_background.y = self.GetScaledY(self.y)
            self._hud_background.draw()
        
        for label, x, y in self._lables:
            label.x = self.GetScaledX(self.x + x)
            label.y = self.GetScaledY(self.y - self._hud_background.image.height + y)
            label.draw()

class Player(Actor, Oscillator):
    '''
    The main player object. This derives from Oscillator and adds in sprite rendering capabilities.
    This is the rendering side of the Oscillator object.
    '''
    
    entity_type = TYPE_PLAYER_SHIP
    
    def __init__(self, parent_level):
        sprite_image = data.load_image('Ship.png')
        sprite_image.anchor_y = sprite_image.height/2  
        Actor.__init__(self, sprite_image, parent_level)
        Oscillator.__init__(self)
        self.x = PLAYER_OFFFSET_FROM_RIGHT_SCREEN_BOUND
        self.y = SIZE_OF_GAMESPACE_Y//2
        self.z = 1 #draw this above other stuff
        
        self._original_color = self.sprite.color
        self.line_color = (1,1,1,1)
        self.shield = 100

    def getHudContents(self):
        return ["Shields:{0}".format(self.shield)]
        
    def Rescale(self, NewScaleFactor):
        super(Player, self).Rescale(NewScaleFactor)

    def Tick(self, delta_t):
        Oscillator.Tick(self, delta_t)
        shipPos = self.GetCurrentValue()
        self.y  = SIZE_OF_GAMESPACE_Y//2 + (shipPos * SIZE_OF_GAMESPACE_Y//2)
        
    def handle_input(self, keys):
        if keys[key.UP] and not keys[key.DOWN]:
            self.AmplitudeAdjust = INCREASE
        elif keys[key.DOWN] and not keys[key.UP]:
            self.AmplitudeAdjust = DECREASE
        else:
            self.AmplitudeAdjust = CONSTANT

        if keys[key.LEFT] and not keys[key.RIGHT]:
            self.FrequencyAdjust = DECREASE
        elif keys[key.RIGHT] and not keys[key.LEFT]:
            self.FrequencyAdjust = INCREASE
        else:
            self.FrequencyAdjust = CONSTANT

        if keys[key.SPACE]:
            self.frozen = True
        else: 
            self.frozen = False
        
    def reset_color(self):
        self.sprite.color = self._original_color

    def on_collision(self):
        self.sprite.color = (255, 0, 0)
        self.shield -= 5

    def get_collidable(self):
        return SpriteCollision(self.sprite) 

    def draw(self):
        Actor.draw(self)
        self.sprite.x = self.GetScaledX(self.x)
        self.sprite.y = self.GetScaledY(self.y)
        #self.sprite.rotation = -self.GetAngle()
        self.draw_path()
        self.sprite.draw()
        if DEBUG:
            draw_bounding_box(self.sprite)
        
    def draw_path(self):
        glColor4f(*self.line_color) 
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        for time in arange(0, SECONDS_TO_CROSS_GAMESPACE, 0.2/self._Omega):
            t, y, a = self.GetPredictiveCoordinate(time)
            x = self.GetScaledX(SIZE_OF_GAMESPACE_X * t/float(SECONDS_TO_CROSS_GAMESPACE) + self.x + self.sprite.width)
            y = self.GetScaledY(SIZE_OF_GAMESPACE_Y//2 + (y * SIZE_OF_GAMESPACE_Y//2))
            glVertex2f(x,y)
        glEnd()
        glLineWidth(1)
        glColor4f(1, 1, 1, 1) 

