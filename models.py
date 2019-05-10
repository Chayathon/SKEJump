
import time
import collections
from random import randint


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


def rand_map(lst):
    index = randint(0, len(lst)-1)
    return lst[index]


def has_tree():
    tree = randint(0, 2)
    if tree == 1:
        return True
    return False


def save_highscore(score):
    high_score = open('score.txt').read()

    if int(score) > int(high_score):

        with open('score.txt','w') as s:
            s.write(score)
            s.write('\n')
            s.close()
    