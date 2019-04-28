import time
import arcade
from random import randint
from models import FPSCounter, rand_map, has_tree

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GROUND = 80
JUMP_SPEED = 10
MOVEMENT_SPEED = 10

map1 = list(reversed(open('map_0.txt').read().splitlines()))
map2 = list(reversed(open('map_1.txt').read().splitlines()))
map3 = list(reversed(open('map_2.txt').read().splitlines()))
platform = list(map(lambda x, y: x+y, map1, map2))

list_map = [map1, map2, map3]


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='SKE Jump (Demo)')

        self.BG = arcade.Sprite(filename='images/backgroundForest.png',
                                center_x=SCREEN_WIDTH//2,
                                center_y=SCREEN_HEIGHT//2)

        self.player = Player('images/SKE_N.png')

        self.map = Map()

        # self.tree = TreeSprite('images/treePineFrozen.png')

        self.physics = arcade.PhysicsEnginePlatformer(self.player,
                                                      self.map)

        self.score = 0

        self.fps = FPSCounter()

    def hits(self):
        for block in self.map:
            if block.is_tree:
                if arcade.check_for_collision(self.player, block):
                    self.player.is_dead = True

    def update(self, delta):
        self.hits()
        self.player.update()

        if not self.player.is_dead:
            self.score += 1
            # self.tree.update()
            self.physics.update()
            self.map.update_animation()
            self.map.check_end_map()

    def on_draw(self):
        arcade.start_render()

        self.BG.draw()

        self.player.draw()

        # self.tree.draw()

        self.map.draw()

        arcade.draw_text(str(self.score),
                         self.width//2, self.height - 40,
                         arcade.color.WHITE, 30)

        self.fps.tick()

        arcade.draw_text(f'fps {self.fps.get_fps():.0f} ms',
                         SCREEN_WIDTH - 70, SCREEN_HEIGHT - 20,
                         arcade.color.RED, 10)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if self.physics.can_jump():
                self.player.change_y = JUMP_SPEED


class Player(arcade.Sprite):
    def __init__(self, file_name):
        super().__init__(filename=file_name, scale=0.5)

        # Create SKE normal state at textures index 0
        self.ske_n = arcade.load_texture(file_name)
        self.textures.append(self.ske_n)

        self.status = 0
        self.center_x = 100
        self.center_y = GROUND

        self.change_angle = 1

        self.is_dead = False

    def update(self):
        self.fall()

    def fall(self):
        if self.center_y < 30:
            self.is_dead = True


class TreeSprite(arcade.Sprite):
    NUM = 0
    def __init__(self, file_name, model_x=600,
                 model_y=GROUND, end_map=False):
        super().__init__(filename=file_name, scale=0.3,
                         center_x=model_x, center_y=model_y)

        self.end_map = end_map
        self.is_tree = has_tree()
        TreeSprite.NUM += 1
        self.num = TreeSprite.NUM

    # def update(self):
    #     self.center_x -= MOVEMENT_SPEED

    #     if self.center_x < -30:
    #         self.center_x = randint(SCREEN_WIDTH + 20,
    #                                 SCREEN_WIDTH + 100)

    #         self.center_y = GROUND

    def update_animation(self):
        self.center_x -= MOVEMENT_SPEED
        print(self.is_tree, ' ', self.num)

        if not self.is_tree:
            self.kill()

        if self.center_x < (-790):
            self.kill()


class Block(arcade.Sprite):
    def __init__(self, file_name, model_x, model_y, end_map=False):
        super().__init__(filename=file_name,
                         center_x=model_x,
                         center_y=model_y,
                         scale=2.0/7.0)
        self.end_map = end_map
        self.is_tree = False

    def update_animation(self):
        self.center_x -= MOVEMENT_SPEED

        if self.center_x < (-790):
            self.kill()


class Map(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.generate_map()

        self.count_block = 0

    def check_end_map(self):
        for block in self.sprite_list:
            if block.end_map and block.center_x <= -10:
                block.end_map = False
                self.new_map()

    def generate_map(self):
        for i in range(len(platform)):
            for j in range(len(platform[i])):
                if platform[i][j] == 'P':
                    self.append(Block('images/slice01.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'N':
                    self.append(Block('images/slice01.png',
                                      10 + j * 20,
                                      10 + i * 20,
                                      True))

                elif platform[i][j] == '0':
                    self.append(Block('images/slice33.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'U':
                    self.append(Block('images/slice07.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'D':
                    self.append(Block('images/slice06.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'u':
                    self.append(Block('images/slice18.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'd':
                    self.append(Block('images/slice17.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'T':
                    self.append(Block('images/slice21.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'B':
                    self.append(Block('images/slice22.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'L':
                    self.append(Block('images/slice23.png',
                                      10 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'l':
                    self.append(Block('images/slice19.png',
                                      10 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'R':
                    self.append(Block('images/slice24.png',
                                      10 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'r':
                    self.append(Block('images/slice20.png',
                                      10 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == '3':
                    self.append(TreeSprite('images/treePineFrozen.png',
                                        10 + j * 20,
                                        10 + i * 20))

    def new_map(self):
        platform = rand_map(list_map)
        for i in range(len(platform)):
            for j in range(len(platform[i])):
                if platform[i][j] == 'P':
                    self.append(Block('images/slice01.png',
                                      790 + j * 20,
                                      10 + i * 20,))

                elif platform[i][j] == 'N':
                    self.append(Block('images/slice01.png',
                                      790 + j * 20,
                                      10 + i * 20,
                                      True))

                elif platform[i][j] == '0':
                    self.append(Block('images/slice33.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'U':
                    self.append(Block('images/slice07.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'D':
                    self.append(Block('images/slice06.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'u':
                    self.append(Block('images/slice18.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'd':
                    self.append(Block('images/slice17.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'T':
                    self.append(Block('images/slice21.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == 'B':
                    self.append(Block('images/slice22.png',
                                      790 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'L':
                    self.append(Block('images/slice23.png',
                                      790 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'l':
                    self.append(Block('images/slice19.png',
                                      790 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'R':
                    self.append(Block('images/slice24.png',
                                      790 + j * 20,
                                      10 + i * 20))
                
                elif platform[i][j] == 'r':
                    self.append(Block('images/slice20.png',
                                      790 + j * 20,
                                      10 + i * 20))

                elif platform[i][j] == '3':
                    self.append(TreeSprite('images/treePineFrozen.png',
                                        790 + j * 20,
                                        10 + i * 20))


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
