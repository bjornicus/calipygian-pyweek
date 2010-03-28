'''
@author: bjorn
'''
import pyglet
import gamestate
import math


##FIXME Temporary testing hacks Remove these!
playership = gamestate.ship()

def TestAdjustAmp(dt):
    print("Adjusting Ship Amplitude")
    playership.AdjustAmplitude(.4)

def TestAdjustFreq(dt):
    print("Adjusting Ship Frequency")
    playership.AdjustAngularFrequency(.7 * math.pi)

def TestAdjustPhase(dt):
    print("Adjusting Ship Phase")
    playership.AdjustPhase( math.pi )
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

    def on_draw(self):
        self.window.clear()
        for i in self.renderlist:
            i.draw()

    def on_key_press(self, symbol, modifiers):
        pass

class LevelOne(LevelBase):
    '''
    Level One
    '''
    def __init__(self, window):
        LevelBase.__init__(self, window)
        label = pyglet.text.Label('LEVEL 1!')
        self.renderlist.append(label)
        
        ## More Test Hacks
        self.shiplabel = pyglet.text.Label('Ship', x=0, y=self.window.height//2)
        
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        pyglet.clock.schedule_once(TestAdjustAmp, 5.0)
        pyglet.clock.schedule_once(TestAdjustFreq, 10.0)
        pyglet.clock.schedule_once(TestAdjustPhase, 15.0)
        
    def update(self, dt):
        ##Temporary hack, we need to come up with a better way of managing gamestate
        playership.Update(dt)
        
        
    def on_draw(self):
        LevelBase.on_draw(self)
        
        ##Yet More Hacking
        shipPos = playership.GetPosition()
        shipPosInWindow = self.window.height//2 + (shipPos * self.window.height//2)
        self.shiplabel.y=shipPosInWindow
        self.shiplabel.draw()
