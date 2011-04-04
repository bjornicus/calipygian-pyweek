UPDATE_RATE = 60 #Update GameState logic 60 times per second
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 360

import pyglet
from pyglet import clock
from spaces import CordinateSpace

import random
import platformer
import puzzle

MOUSE_EVENT_PRESS = 1
MOUSE_EVENT_RELEASE = 2
MOUSE_EVENT_DRAG = 3

def run():
    pyglet.resource.path = ['data','design']
    pyglet.resource.reindex()

    root_game_space = CordinateSpace()
    platformer.setup_platformer(root_game_space)
    puzzle.setup_puzzles(root_game_space)

    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    @window.event
    def on_draw():
        window.clear()
        for GameObj in root_game_space:
            cord = root_game_space.GetCordinatesOfContainedObject(GameObj)
            #here we can insert the logic for scaling!
            if cord is not None:
                GameObj.Draw((cord.get_x(), cord.get_y()))

    @window.event
    def on_mouse_press(x, y, buttons, modifiers):
        root_game_space.on_mouse_event(MOUSE_EVENT_PRESS, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_mouse_release(x, y, buttons, modifiers):
        root_game_space.on_mouse_event(MOUSE_EVENT_RELEASE, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        root_game_space.on_mouse_event(MOUSE_EVENT_DRAG, x, y, 0, 0, buttons, modifiers)


    def update(dt):
        root_game_space.Update(dt)

    clock.schedule_interval_soft(update, 1.0 / UPDATE_RATE)
        
    pyglet.app.run()

