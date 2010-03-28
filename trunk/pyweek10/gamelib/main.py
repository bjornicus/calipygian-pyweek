'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pyglet
from levels import *

def main():
    window = pyglet.window.Window()
    level1 = LevelOne(window)
    window.push_handlers(level1)
    pyglet.app.run()
