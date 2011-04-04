import pyglet
from pyglet.gl import *
from pyglet import clock
from spaces import CordinateSpace, SpaceCordinate
from constants import *
import platformer
import puzzle
from puzzle import PUZZLE_BLOCK_SIDE_PIXEL_LENGTH


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

class GameState():
    def __init__(self):
        pyglet.resource.path = ['data','design']
        pyglet.resource.reindex()

        self.root_draw_location = None
       

        self.root_game_space = CordinateSpace()
        platformspace = platformer.setup_platformer()
        puzzlespace = puzzle.setup_puzzles()
        self.root_game_space.AddObject(puzzlespace, 0, 0)
        self.root_game_space.AddObject(platformspace, 0, PUZZLE_BLOCK_SIDE_PIXEL_LENGTH)

    def update(self, dt):
        self.root_game_space.Update(dt)

class PlatformWindow():
    def __init__(self, GameState):
        
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.window = create_game_window(self, self.width, self.height)
        
        self.GameState = GameState
        self.update_location()
        
        self.GameState.master_window = self
        self.current_mouse_gesture = None

    def update_location(self):
        x,y = self.window.get_location()

        y += self.height

        self.GameState.root_draw_location = (x,y)
         

    def on_move(self, x, y):
        self.update_location()
        
    def on_draw(self):
        for GameObj in self.GameState.root_game_space:
            cord = self.GameState.root_game_space.GetCordinatesOfContainedObject(GameObj)
            #here we can insert the logic for scaling!
            if cord is not None:
                GameObj.Draw((cord.get_x(), cord.get_y()))
                
    def mouse_gesture_handler(self, Event_Type, x, y, dx, dy, buttons, modifiers):
        if buttons is pyglet.window.mouse.LEFT:
            if Event_Type is MOUSE_EVENT_PRESS:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.abort()
                    self.current_mouse_gesture = None
                else:
                    self.current_mouse_gesture = MouseGesture(self.GameState.root_game_space, x, y)
            elif Event_Type is MOUSE_EVENT_RELEASE:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.release(x,y)
                    self.current_mouse_gesture = None
            elif Event_Type is MOUSE_EVENT_DRAG:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.update(x,y)

        Chord = SpaceCordinate(self.GameState.root_game_space, x, y)
        self.GameState.root_game_space.on_mouse_event(Event_Type,
                                            Chord,
                                            buttons,
                                            modifiers,
                                            self.current_mouse_gesture)

class PuzzleWindow():
    def __init__(self, GameState):
        self.width = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
        self.height = PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
        self.window = create_game_window(self, self.width, self.height)

        self.GameState = GameState
        self.current_mouse_gesture = None
        self.location = None

        
    def on_draw(self):
        root_x, root_y = self.GameState.root_draw_location
        window_x, window_y = self.get_location()

        dx = window_x - root_x
        dy = window_y - root_y
        
        for GameObj in self.GameState.root_game_space:
            cord = self.GameState.root_game_space.GetCordinatesOfContainedObject(GameObj)
            #TODO, NEED TO WRITE CULLING LOGIC!
            if cord is not None:
                GameObj.Draw((cord.get_x() - dx, cord.get_y() + dy))


    def get_location(self):
        x,y = self.window.get_location()
        y += self.height
        return (x,y)


    def on_move(self, x, y):
        pass
    
    def mouse_gesture_handler(self, Event_Type, x, y, dx, dy, buttons, modifiers):
        root_x, root_y = self.GameState.root_draw_location
        window_x, window_y = self.get_location()

        x += window_x - root_x
        y -= window_y - root_y
        
        if buttons is pyglet.window.mouse.LEFT:
            if Event_Type is MOUSE_EVENT_PRESS:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.abort()
                    self.current_mouse_gesture = None
                else:
                    self.current_mouse_gesture = MouseGesture(self.GameState.root_game_space, x, y)
            elif Event_Type is MOUSE_EVENT_RELEASE:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.release(x,y)
                    self.current_mouse_gesture = None
            elif Event_Type is MOUSE_EVENT_DRAG:
                if self.current_mouse_gesture is not None:
                    self.current_mouse_gesture.update(x,y)

        Chord = SpaceCordinate(self.GameState.root_game_space, x, y)
        self.GameState.root_game_space.on_mouse_event(Event_Type,
                                            Chord,
                                            buttons,
                                            modifiers,
                                            self.current_mouse_gesture) 

def create_game_window(GameObject, Width, Height):
    window = pyglet.window.Window(Width, Height)
    glClearColor(0.4,1.0, 1.0, 1.0)
    
    @window.event
    def on_mouse_press(x, y, buttons, modifiers):
        GameObject.mouse_gesture_handler(MOUSE_EVENT_PRESS, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_mouse_release(x, y, buttons, modifiers):
        GameObject.mouse_gesture_handler(MOUSE_EVENT_RELEASE, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        GameObject.mouse_gesture_handler(MOUSE_EVENT_DRAG, x, y, 0, 0, buttons, modifiers)

    @window.event
    def on_move(x, y):
        GameObject.on_move(x, y)

    @window.event
    def on_draw():
        window.clear()
        GameObject.on_draw()
    return window

def run():
    state = GameState()
    master_game_window = PlatformWindow(state)

    window2 = PuzzleWindow(state)

    def update(dt):
        state.update(dt)

    clock.schedule_interval_soft(update, 1.0 / UPDATE_RATE)
    pyglet.app.run()

