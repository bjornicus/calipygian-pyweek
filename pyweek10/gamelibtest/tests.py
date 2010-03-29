'''
@author: bjorn
'''
from numpy.testing.utils import *
from gamelib.levels import *
from gamelib.gamestate import *
import math

from pyglet.window import key

def test_LevelBase_on_draw_clears_window():
    class mock_Window:
        def clear(self):
            self.clear_called = True
        def push_handlers(self, handler):
            pass

    mockWindow = mock_Window()
    base = LevelBase(mockWindow)
    base.on_draw()

    assert mockWindow.clear_called
 
def test_LevelBase_on_draw_calls_draw_on_all_items_in_renderlist():
    class mock_Window:
        def clear(self):
            pass
        def push_handlers(self, handler):
            pass

    class mock_drawable:
        def draw(self):
            self.draw_called = True

    drawable1 = mock_drawable()
    drawable2 = mock_drawable()
    base = LevelBase(mock_Window())
    base.renderlist.append(drawable1)
    base.renderlist.append(drawable2)
    base.on_draw()

    assert drawable1.draw_called
    assert drawable2.draw_called

#------------- oscillator tests --------------#
def test_Oscillator_AdjustFrequency_does_not_change_position():
    oscillator = Oscillator()
    oscillator._Omega = gamestate.MIN_FREQUENCY
      
    for t_step in range(0,200):
        
        old_x = oscillator.GetPosition()
        oscillator.AdjustAngularFrequency(0)
        new_x = oscillator.GetPosition()
        assert abs(old_x - new_x) < 0.01
        
        for f_step in [0.01, 0.05, 0.1, 0.5]:
            while (oscillator._Omega + f_step < gamestate.MAX_FREQUENCY):
                old_x = oscillator.GetPosition()
                oscillator.AdjustAngularFrequency(f_step)
                new_x = oscillator.GetPosition()
                assert abs(old_x - new_x) < 0.01
                
            while (oscillator._Omega - f_step > gamestate.MIN_FREQUENCY):
                old_x = oscillator.GetPosition()
                oscillator.AdjustAngularFrequency(-f_step)
                new_x = oscillator.GetPosition()
                assert abs(old_x - new_x) < 0.01
        oscillator.Tick(0.01, pyglet.window.key.KeyStateHandler())

def test_Oscillator_AdjustAmplitude_does_not_change_position():
    oscillator = Oscillator()
    oscillator._Amplitude = gamestate.MIN_AMPLITUDE
          
    for t_step in range(0,200):
        
        old_x = oscillator.GetPosition()
        oscillator.AdjustAmplitude(0)
        new_x = oscillator.GetPosition()
        assert abs(old_x - new_x) < 0.01
        
        for a_step in [.01*math.pi, .05*math.pi, .1*math.pi, .5*math.pi]:
            while (oscillator._Amplitude + a_step < gamestate.MAX_AMPLITUDE):
                old_x = oscillator.GetPosition()
                oscillator.AdjustAmplitude(a_step)
                new_x = oscillator.GetPosition()
                assert abs(old_x - new_x) < 0.01
                
            while (oscillator._Amplitude - a_step > gamestate.MIN_AMPLITUDE):
                old_x = oscillator.GetPosition()
                oscillator.AdjustAmplitude(-a_step)
                new_x = oscillator.GetPosition()
                assert abs(old_x - new_x) < 0.01
        oscillator.Tick(0.01, pyglet.window.key.KeyStateHandler())
        

print("Starting Oscillator Tests")
print("Starting Oscillator test_Oscillator_AdjustFrequency_does_not_change_position")
test_Oscillator_AdjustFrequency_does_not_change_position()
print("Starting test_Oscillator_AdjustAmplitude_does_not_change_position")
test_Oscillator_AdjustAmplitude_does_not_change_position()