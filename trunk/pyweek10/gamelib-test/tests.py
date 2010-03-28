'''
@author: bjorn
'''
from numpy.testing.utils import *
from gamelib.levels import *

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
