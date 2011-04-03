import pyglet
from spaces import *

DefaultGameSpace = CordinateSpace()

class TestLabel(GameObject):
    GameObjectType = "Label"
    
    def __init__(self):
        GameObject.__init__(self)
        self.label = pyglet.text.Label('Hello, world', 
                                        font_name='Times New Roman', 
                                        font_size=36,
                                        color=(0,0,0,255),
                                        anchor_x='center', anchor_y='center')

    def Draw(self, xy_pos):
        self.label.x, self.label.y = xy_pos
        self.label.draw()

class TestBackground(GameObject):
    GameObjectType = "BG"
    
    def __init__(self):
        GameObject.__init__(self)
        self.image = pyglet.resource.image('playfield.png')

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.image.blit(x,y)
    
def run():
    window = pyglet.window.Window(810, 360)

    pyglet.resource.path = ['data','design']
    pyglet.resource.reindex()
    DefaultGameSpace.AddObject(TestLabel(), window.width//2, y=window.height//2)
    DefaultGameSpace.AddObject(TestBackground())   

    @window.event
    def on_draw():
        window.clear()
        for GameObj in DefaultGameSpace:
            cord = DefaultGameSpace.GetCordinatesOfContainedObject(GameObj)
            #here we can insert the logic for scaling!
            GameObj.Draw((cord.get_x(), cord.get_y()))
        
    pyglet.app.run()

