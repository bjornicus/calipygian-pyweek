'''
@author: bjorn
'''
import pyglet

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
