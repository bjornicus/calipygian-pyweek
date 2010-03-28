'''
@author: bjorn
'''
import pyglet
from pyglet.window import key

import gamestate
import math

##FIXME Temporary testing hacks Remove these!
playership = gamestate.oscillator()
shiplabel = pyglet.text.Label('Ship', x=0, y=240)

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
        self.renderlist = []
        self.actorlist = []
        self.renderlist.append(shiplabel)
        self.actorlist.append(playership)
        
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def on_draw(self):
        self.window.clear()
        for drawable in self.renderlist:
            drawable.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            playership.AmplitudeAdjust = gamestate.AMPLITUDE_INCREASE
        elif symbol == key.DOWN:
            playership.AmplitudeAdjust = gamestate.AMPLITUDE_DECREASE
        elif symbol == key.RIGHT:
            playership.FrequencyAdjust = gamestate.FREQUENCY_INCREASE
        elif symbol == key.LEFT:
            playership.FrequencyAdjust = gamestate.FREQUENCY_DECREASE

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            playership.AmplitudeAdjust = gamestate.AMPLITUDE_STEADY
        elif symbol == key.DOWN:
            playership.AmplitudeAdjust = gamestate.AMPLITUDE_STEADY
        elif symbol == key.RIGHT:
            playership.FrequencyAdjust = gamestate.FREQUENCY_STEADY
        elif symbol == key.LEFT:
            playership.FrequencyAdjust = gamestate.FREQUENCY_STEADY
        
    def update(self, dt):
        for actor in self.actorlist:
            actor.Update(dt)

class LevelOne(LevelBase):
    '''
    Level One
    '''
    def __init__(self, window):
        LevelBase.__init__(self, window)
        
    def on_draw(self):
        LevelBase.on_draw(self)
        
        ##Yet More Hacking
        shipPos = playership.GetPosition()
        shipPosInWindow = self.window.height//2 + (shipPos * self.window.height//2)
        shiplabel.y=shipPosInWindow
