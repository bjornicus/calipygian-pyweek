import pyglet
from pyglet import clock
from spaces import CordinateSpace, SpaceCordinate
from constants import *
import random
import platformer
import puzzle


class MouseGesture():
    def __init__(self, space, depress_x, depress_y):
        self.space = space
        self.depress_cord = SpaceCordinate(self.space, depress_x, depress_y)

        self.release_cord = None

        self.current_cord = SpaceCordinate(self.space, depress_x, depress_y)

        self.state = MOUSE_GESTURE_STARTED

    def update(self, current_x, current_y):
        self.current_cord.set_x(current_x)
        self.current_cord.set_y(current_y)

    def release(self, release_x, release_y):
        self.release_cord = SpaceCordinate(self.space, release_x, release_y)
        self.state = MOUSE_GESTURE_COMPLETED

    def abort(self):
        self.depress_cord = None
        self.release_cord = None
        self.current_cord = None

        self.state = MOUSE_GESTURE_ABORTED


class Game():
    def __init__(self):
        pyglet.resource.path = ['data','design']
        pyglet.resource.reindex()

        self.root_game_space = CordinateSpace()
        platformer.setup_platformer(self.root_game_space)
        puzzle.setup_puzzles(self.root_game_space)

        self.current_mouse_gesture = None
        
    def on_draw(self):
        for GameObj in self.root_game_space:
            cord = self.root_game_space.GetCordinatesOfContainedObject(GameObj)
            #here we can insert the logic for scaling!
            if cord is not None:
                GameObj.Draw((cord.get_x(), cord.get_y()))

    def update(self, dt):
        self.root_game_space.Update(dt)

    def mouse_gesture_handler(self, Event_Type, x, y, dx, dy, buttons, modifiers):
        if buttons is pyglet.window.mouse.LEFT:
            if Event_Type is MOUSE_EVENT_PRESS:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.abort()
                    self.current_mouse_gesture = None
                else:
                    self.current_mouse_gesture = MouseGesture(self.root_game_space, x, y)
            elif Event_Type is MOUSE_EVENT_RELEASE:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.release(x,y)
                    self.current_mouse_gesture = None
            elif Event_Type is MOUSE_EVENT_DRAG:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.update(x,y)

        Chord = SpaceCordinate(self.root_game_space, x, y)
        self.root_game_space.on_mouse_event(Event_Type,
                                            Chord,
                                            buttons,
                                            modifiers,
                                            self.current_mouse_gesture) 


def run():
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = Game()
    @window.event
    def on_mouse_press(x, y, buttons, modifiers):
        game.mouse_gesture_handler(MOUSE_EVENT_PRESS, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_mouse_release(x, y, buttons, modifiers):
        game.mouse_gesture_handler(MOUSE_EVENT_RELEASE, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        game.mouse_gesture_handler(MOUSE_EVENT_DRAG, x, y, 0, 0, buttons, modifiers)

    def update(dt):
        game.update(dt)

    @window.event
    def on_draw():
        window.clear()
        game.on_draw()

    clock.schedule_interval_soft(update, 1.0 / UPDATE_RATE)
    pyglet.app.run()

