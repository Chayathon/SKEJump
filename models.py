import arcade.key
import time, collections
from random import randint

# N_JUMP = 0

# KEY_OFFSETS = {N_JUMP: 150}

# KEY_MAP = {arcade.key.SPACE : N_JUMP}


# GRAVITY = 10
# GROUND = 175
# MOVEMENT_SPEED = 10


# class SKEman:
#     def __init__(self, world, x, y):
#         self.world = world
#         self.x = x
#         self.y = y

#         self.y_before2jump = 0

#         self.jump = False
#         self.p_jump = False

#         self.jump_counting = 0

#         self.key = False

#         self.is_dead = False
    
#     def die(self):
#         self.is_dead = True


#     def update(self, delta):
#         if self.jump:

#             if self.world.ground + KEY_OFFSETS[N_JUMP] > self.y and self.jump_counting == 1:
#                 self.y += 10

#             elif self.y_before2jump + KEY_OFFSETS[N_JUMP] > self.y and self.jump_counting == 2:
#                 self.y += 10

#             else:
#                 self.jump = False
#                 self.key = False
        
#         if self.y == self.world.ground:
#             self.jump_counting = 0
        
#         elif self.y > self.world.ground and not self.jump:
#             self.y -= GRAVITY


#     def check_key(self, key_offsets):
#         if key_offsets == 0:
#             self.jump = True
#             self.key = True
#             self.jump_counting += 1

#             if self.jump_counting == 2:
#                 self.y_before2jump = self.y
        

# class World:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height

#         # self.barrier = Barrier(self, 600, GROUND+20)

#         self.ske = SKEman(self, 200, GROUND)

#         self.ground = GROUND
#         self.gravity = GRAVITY

#         self.score = 0

#     def add_score(self):
#         self.score += 1

#     def update(self, delta):
#         self.ske.update(delta)

#         # self.barrier.update()

#         self.add_score()

#     def on_key_press(self, key, key_modifiers):
#         if key in KEY_MAP:
#             self.ske.check_key(KEY_MAP[key])


# class Barrier:
#     def __init__(self, world, x, y):
#         self.x = x
#         self.y = y
#         self.world = world

#     def update(self):
#         self.x -= MOVEMENT_SPEED

#         if self.x <= 0:
#             from random import randint
#             from SKEJump import SCREEN_WIDTH
#             self.x = randint(self.world.ske.x + SCREEN_WIDTH + 30,
#                              self.world.ske.x + SCREEN_WIDTH + 100)


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)