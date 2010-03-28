'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pyglet
from levels import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

def main():
    window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    level1 = LevelOne(window)
    window.push_handlers(level1)
    pyglet.app.run()
