import arcade.key
from random import randint

N_JUMP = 0
P_JUMP = 1

KEY_OFFSETS = {N_JUMP: 120,
                P_JUMP: 200}

KEY_MAP = {arcade.key.SPACE : N_JUMP,
            arcade.key.UP : P_JUMP}


GRAVITY = 5
GROUND = 140
MOVEMENT_SPEED = 5

class SKEman:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

        self.jump = False
        self.p_jump = False

        self.key = False

    def update(self, delta):
        if self.y > GROUND and not self.key:
            self.y -= GRAVITY
        
        if self.jump:
            if GROUND + KEY_OFFSETS[N_JUMP] > self.y:
                self.y += 5
            else:
                self.jump = False
                self.key = False
        
        elif self.p_jump:
            if GROUND + KEY_OFFSETS[P_JUMP] > self.y:
                self.y += 5
            else:
                self.p_jump = False
                self.key = False


    def check_key(self, key_offsets):
        if key_offsets == 0:
            self.jump = True
            self.key = True
        
        elif key_offsets == 1:
            self.p_jump = True
            self.key = True
        

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
        if self.ske.y == GROUND:
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