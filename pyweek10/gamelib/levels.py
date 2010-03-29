'''
@author: bjorn
'''
import pyglet
from pyglet.window import key

import gamestate

##FIXME Temporary testing hacks Remove these!
playership = gamestate.Oscillator()
shiplabel = pyglet.text.Label('Ship', x=0, y=240)
predictive_label = pyglet.text.Label('-')

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
        
        self.renderlist.append(shiplabel)
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
        
        for (t, y) in playership.GetPredictivePath(.1, 2.0, .01):
            offset = self.window.width * (t/2.0)
            predictive_label.y = self.window.height//2 + (y * self.window.height//2)
            predictive_label.x = offset
            predictive_label.draw()
            
