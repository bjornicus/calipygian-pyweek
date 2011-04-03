import pyglet

def run():
    window = pyglet.window.Window(810, 360)

    label = pyglet.text.Label('Hello, world', 
                              font_name='Times New Roman', 
                              font_size=36,
                              color=(0,0,0,255),
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    pyglet.resource.path = ['data','design']
    pyglet.resource.reindex()
    image = pyglet.resource.image('playfield.png')

    @window.event
    def on_draw():
        window.clear()
        image.blit(0,0)
        label.draw()

    pyglet.app.run()

