import aracde.key

MOVEMENT_SPEED = 5

class SKEman:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def update(self, delta):
        pass


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.man = SKEman(self, width//2, height//2)

        self.score = 0

    def update(self, delta):
        pass