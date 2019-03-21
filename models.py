import arcade.key
from random import randint

N_JUMP = 0

KEY_OFFSETS = {N_JUMP: 120}

KEY_MAP = {arcade.key.SPACE : N_JUMP}


GRAVITY = 10
GROUND = 140
MOVEMENT_SPEED = 5

class SKEman:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

        self.y_before2jump = 0

        self.jump = False
        self.p_jump = False

        self.jump_counting = 0

        self.key = False

    def update(self, delta):
        if self.y > GROUND and not self.key:
            self.y -= GRAVITY
        
        if self.jump and self.jump_counting == 1:
            if GROUND + KEY_OFFSETS[N_JUMP] > self.y:
                self.y += 10
            else:
                self.jump = False
                self.key = False
        
        elif self.jump and self.jump_counting == 2:
            if self.y_before2jump + KEY_OFFSETS[N_JUMP] > self.y:
                self.y += 10
            else:
                self.jump = False
                self.key = False

        else:
            self.jump = False
            self.key = False
        
        if self.y == GROUND:
            self.jump_counting = 0


    def check_key(self, key_offsets):
        if key_offsets == 0:
            self.jump = True
            self.key = True
            self.jump_counting += 1

            if self.jump_counting == 2:
                self.y_before2jump = self.y
        

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.ske = SKEman(self, 200, GROUND)

        self.slope = Slope(self, randint(850, 900), 100)

        self.score = 0

    def add_score(self):
        self.score += 1

    def update(self, delta):
        self.ske.update(delta)

        self.slope.update(delta)

        self.add_score()

    def on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ske.check_key(KEY_MAP[key])



class Wolf:
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world
    
    def update(self):
        self.x -= MOVEMENT_SPEED


class Tree:
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world

    def update(self):
        self.x -= MOVEMENT_SPEED


class Barier:
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world
    
    def update(self):
        self.x -= MOVEMENT_SPEED


class Slope:
    def __init__(self, world, x, y):
        self.x = x
        self.y = y
        self.world = world

    def update(self, delta):
        self.x -= MOVEMENT_SPEED