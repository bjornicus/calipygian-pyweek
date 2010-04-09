'''
@author: bjorn
'''
from numpy.testing.utils import *
from gamelib.levels import *
from gamelib.entities import *
from gamelib.constants import *
import math

from pyglet.window import key
import oscillator

def test_Levellevelbase_on_draw_clears_window():
    class mock_Window:
        def clear(self):
            self.clear_called = True
        def push_handlers(self, handler):
            pass

    mockWindow = mock_Window()
    levelbase = LevelBase()
    levelbase.window = mockWindow
    levelbase.on_draw()

    assert mockWindow.clear_called
 
#------------- oscillator tests --------------#
def test_Oscillator_AdjustFrequency_does_not_change_position():
    oscillator = oscillator.Oscillator()
    oscillator._Omega = MIN_FREQUENCY
      
    for t_step in range(0,200):
        
        old_x = oscillator.GetCurrentValue()
        oscillator.AdjustAngularFrequency(0)
        new_x = oscillator.GetCurrentValue()
        assert abs(old_x - new_x) < 0.01
        
        for f_step in [0.01, 0.05, 0.1, 0.5]:
            while (oscillator._Omega + f_step < MAX_FREQUENCY):
                old_x = oscillator.GetCurrentValue()
                oscillator.AdjustAngularFrequency(f_step)
                new_x = oscillator.GetCurrentValue()
                assert abs(old_x - new_x) < 0.01
                
            while (oscillator._Omega - f_step > MIN_FREQUENCY):
                old_x = oscillator.GetCurrentValue()
                oscillator.AdjustAngularFrequency(-f_step)
                new_x = oscillator.GetCurrentValue()
                assert abs(old_x - new_x) < 0.01
        oscillator.Tick(0.01, pyglet.window.key.KeyStateHandler())

def test_Oscillator_AdjustAmplitude_does_not_change_position():
    oscillator = oscillator.Oscillator()
    oscillator._Amplitude = MIN_AMPLITUDE
          
    for t_step in range(0,200):
        
        old_x = oscillator.GetCurrentValue()
        oscillator.AdjustAmplitude(0)
        new_x = oscillator.GetCurrentValue()
        assert abs(old_x - new_x) < 0.01
        
        for a_step in [.01*math.pi, .05*math.pi, .1*math.pi, .5*math.pi]:
            while (oscillator._Amplitude + a_step < MAX_AMPLITUDE):
                old_x = oscillator.GetCurrentValue()
                oscillator.AdjustAmplitude(a_step)
                new_x = oscillator.GetCurrentValue()
                assert abs(old_x - new_x) < 0.01
                
            while (oscillator._Amplitude - a_step > MIN_AMPLITUDE):
                old_x = oscillator.GetCurrentValue()
                oscillator.AdjustAmplitude(-a_step)
                new_x = oscillator.GetCurrentValue()
                assert abs(old_x - new_x) < 0.01
        oscillator.Tick(0.01, pyglet.window.key.KeyStateHandler())
        

print("Starting Oscillator Tests")
print("Starting Oscillator test_Oscillator_AdjustFrequency_does_not_change_position")
test_Oscillator_AdjustFrequency_does_not_change_position()
print("Starting test_Oscillator_AdjustAmplitude_does_not_change_position")
test_Oscillator_AdjustAmplitude_does_not_change_position()
