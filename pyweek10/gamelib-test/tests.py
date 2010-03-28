'''
@author: bjorn
'''
from numpy.testing.utils import *
from gamelib.levels import *
from gamelib.gamestate import *
import math

def test_LevelBase_on_draw_clears_window():
    class mock_Window:
        def clear(self):
            self.clear_called = True

    mockWindow = mock_Window()
    base = LevelBase(mockWindow)
    base.on_draw()

    assert mockWindow.clear_called
 
def test_LevelBase_on_draw_calls_draw_on_all_items_in_renderlist():
    class mock_Window:
        def clear(self):
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
    old_x = oscillator.X
    oscillator.AdjustFrequency(1)
    assert old_x == oscillator.X

def test_Oscillator_AdjustAmplitude_does_not_change_position():
    oscillator = Oscillator()
    old_x = oscillator.X
    oscillator.AdjustAmplitude(1)
    assert old_x == oscillator.X

def test_Oscillator_AdjustAmplitude_changes_velocity():
    oscillator = Oscillator()
    old_v = oscillator.Velocity
    oscillator.AdjustAmplitude(1)
    expectedVelocity = 0 + oscillator._Omega**2*oscillator._Amplitude
    assert_equal(oscillator.Velocity, expectedVelocity)
