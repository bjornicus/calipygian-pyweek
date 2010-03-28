'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
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

    def on_draw(self):
        self.window.clear()

    def on_key_press(self, symbol, modifiers):
        pass

class LevelOne(LevelBase):
    '''
    Level One
    '''
    def __init__(self, window):
        LevelBase.__init__(self, window)
        self.label = pyglet.text.Label('LEVEL 1!')

    def on_draw(self):
        LevelBase.on_draw(self)
        self.label.draw()

def main():
    window = pyglet.window.Window()
    level1 = LevelOne(window)
    window.push_handlers(level1)
    pyglet.app.run()
