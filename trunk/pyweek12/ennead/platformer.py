import pyglet
from spaces import GameObject, CordinateSpace
from constants import *
from platformer_level import *
from pyglet.window import key

keystates = key.KeyStateHandler()

def setup_platformer():
    platforspace = CordinateSpace()
    platforspace.width = LEVEL_WIDTH_IN_TILES * TILE_SIZE_IN_PIXELS
    platforspace.height = LEVEL_HEIGHT_IN_TILES * TILE_SIZE_IN_PIXELS
    
    platforspace.AddObject(Level(), 0, 0)
    platforspace.AddObject(Player(), TILE_SIZE_IN_PIXELS, 6*TILE_SIZE_IN_PIXELS)

    return platforspace

class Level(GameObject):
    GameObjectType = "Level"

    def __init__(self):
        GameObject.__init__(self)
        tile_batch = pyglet.graphics.Batch()
        tile_images = {}
        self.sprites = []
        for x in range(0, LEVEL_WIDTH_IN_TILES):
            for y in range(0, LEVEL_HEIGHT_IN_TILES):
                tile_type = level_map_key[level_map[y][x]]
                if tile_type is None:
                    continue
                if not tile_images.has_key(tile_type):
                    tile_images[tile_type] = pyglet.resource.image(tile_type + '.png')
                sprite = pyglet.sprite.Sprite(tile_images[tile_type], batch=tile_batch)
                sprite.x = x * TILE_SIZE_IN_PIXELS
                sprite.y = y * TILE_SIZE_IN_PIXELS + PUZZLE_BLOCK_SIDE_PIXEL_LENGTH
                self.sprites.append(sprite)
        self.tiles = tile_batch

    def Draw(self, xy_pos):
        self.tiles.draw()

class Player(GameObject):
    GameObjectType = "Player"

    def __init__(self):
        GameObject.__init__(self)
        self.sprite = pyglet.resource.image('player.png')
        self.x_vel = 0
        self.y_vel = 0
        self.update_coordinates()

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.blit(x,y)

    def Update(self, dt):
        self.update_coordinates()
        self.apply_gravity(dt)

        if keystates[key.RIGHT]:
            self.move_right(dt)
        elif keystates[key.LEFT]:
            self.move_left(dt)
        elif keystates[key.SPACE]:
            self.jump()
            
        self.cord.set_y(self.cord.get_y() + self.y_vel*dt)
        self.cord.set_x(self.cord.get_x() + self.x_vel*dt)

    def update_coordinates(self):
        self.cord = self.GetCordinatesInParentSpace()

    def apply_gravity(self, dt):
        if self.is_colliding_below():
            self.y_vel = 0
        self.y_vel -= 8*dt

    def is_colliding_below(self):
        x,y = self.cord.get_x(), self.cord.get_y()
        lower_left_tile = find_tile_for_point(x+10,y)
        lower_right_tile = find_tile_for_point(x-10+TILE_SIZE_IN_PIXELS,y)
        if lower_left_tile == 0 and lower_right_tile == 0:
            return False
        return True

    def move_right(self, dt):
        self.cord.set_x(self.cord.get_x() + (20 * dt))

    def move_left(self, dt):
        self.cord.set_x(self.cord.get_x() - (20 * dt))

    def jump(self):
        if self.is_colliding_below():
            self.y_vel = 20

