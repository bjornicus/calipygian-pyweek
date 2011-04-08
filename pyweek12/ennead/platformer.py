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
        tile_spritesheet = pyglet.resource.image('tilesheet.png')
        tile_sequence = pyglet.image.ImageGrid(tile_spritesheet, 4, 5)
        self.sprites = []

        for x in range(0, LEVEL_WIDTH_IN_TILES):
            for y in range(0, LEVEL_HEIGHT_IN_TILES):
                tile_type = level_map[y][x]
                if tile_is_empty(tile_type):
                    continue
                sprite = pyglet.sprite.Sprite(tile_sequence[tile_type], batch=tile_batch)
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
        walk_spritesheet = pyglet.resource.image('player.png')
        walk_sequence = pyglet.image.ImageGrid(walk_spritesheet, 1, 9)
        walk_animation = pyglet.image.Animation.from_image_sequence(walk_sequence, 0.05)
        self.sprite = pyglet.sprite.Sprite(walk_animation)

        self.x_vel = 0
        self.y_vel = 0
        self.update_coordinates()

    def Draw(self, xy_pos):
        x,y = xy_pos
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.draw()

    def Update(self, dt):
        self.update_coordinates()
        self.apply_gravity(dt)
        self.apply_drag(dt)

        if keystates[key.RIGHT]:
            self.move_right(dt)
        if keystates[key.LEFT]:
            self.move_left(dt)
        if keystates[key.SPACE]:
            self.jump()
            
        self.do_not_go_through_ceiling()
        self.do_not_go_through_floor()
        self.do_not_go_through_walls()

        self.cord.set_y(self.cord.get_y() + self.y_vel*dt)
        self.cord.set_x(self.cord.get_x() + self.x_vel*dt)

    def update_coordinates(self):
        self.cord = self.GetCordinatesInParentSpace()

    def apply_gravity(self, dt):
        self.y_vel -= GRAVITY_ACCELERATION*dt
        if self.y_vel < -1*MAX_Y_VEL:
            self.y_vel = -1*MAX_Y_VEL;

    def apply_drag(self, dt):
        if self.is_colliding_below():
            slowdown = dt*GROUND_DRAG
            if slowdown > abs(self.x_vel):
                self.x_vel=0
            else:
                self.x_vel -= self.x_vel/abs(self.x_vel) * slowdown

    def do_not_go_through_floor(self):
        if self.is_colliding_below() and self.y_vel < 0:
            self.y_vel = 0
    
    def do_not_go_through_walls(self):
        if self.is_colliding_on_right() and self.x_vel > 0:
            self.x_vel = 0
        elif self.is_colliding_on_left() and self.x_vel < 0:
            self.x_vel = 0
    
    def do_not_go_through_ceiling(self):
        if self.is_colliding_above() and self.y_vel > 0:
            self.y_vel = 0

    def is_colliding_below(self):
        x_left = self.cord.get_x() + COLLISION_BOX_REDUCTION_IN_PIXELS
        x_right = self.cord.get_x() + TILE_SIZE_IN_PIXELS - COLLISION_BOX_REDUCTION_IN_PIXELS 
        y = self.cord.get_y()
        lower_left_tile_type = find_tile_for_point(x_left, y)
        lower_right_tile_type = find_tile_for_point(x_right, y)
        if tile_is_empty(lower_left_tile_type) and tile_is_empty(lower_right_tile_type):
            return False
        return True

    def is_colliding_above(self):
        x_left = self.cord.get_x() + COLLISION_BOX_REDUCTION_IN_PIXELS
        x_right = self.cord.get_x() + TILE_SIZE_IN_PIXELS - COLLISION_BOX_REDUCTION_IN_PIXELS 
        y = self.cord.get_y() + TILE_SIZE_IN_PIXELS
        upper_left_tile_type = find_tile_for_point(x_left, y)
        upper_right_tile_type = find_tile_for_point(x_right, y)
        if tile_is_empty(upper_left_tile_type) and tile_is_empty(upper_right_tile_type):
            return False
        return True

    def is_colliding_on_right(self):
        x = self.cord.get_x() + TILE_SIZE_IN_PIXELS
        y_bottom = self.cord.get_y() + COLLISION_BOX_REDUCTION_IN_PIXELS
        y_top = self.cord.get_y() + TILE_SIZE_IN_PIXELS - COLLISION_BOX_REDUCTION_IN_PIXELS
        lower_right_tile_type = find_tile_for_point(x, y_bottom)
        upper_right_tile_type = find_tile_for_point(x, y_top)
        if tile_is_empty(lower_right_tile_type) and tile_is_empty(upper_right_tile_type):
            return False
        return True

    def is_colliding_on_left(self):
        x = self.cord.get_x()
        y_bottom = self.cord.get_y() + COLLISION_BOX_REDUCTION_IN_PIXELS
        y_top = self.cord.get_y() + TILE_SIZE_IN_PIXELS - COLLISION_BOX_REDUCTION_IN_PIXELS
        lower_left_tile_type = find_tile_for_point(x, y_bottom)
        upper_left_tile_type = find_tile_for_point(x, y_top)
        if tile_is_empty(lower_left_tile_type) and tile_is_empty(upper_left_tile_type):
            return False
        return True

    def move_right(self, dt):
        self.x_vel = MAX_X_VEL

    def move_left(self, dt):
        self.x_vel = -1*MAX_X_VEL

    def jump(self):
        if self.is_colliding_below():
            self.y_vel = MAX_Y_VEL

