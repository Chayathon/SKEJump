import time
import arcade
import physics
from random import randint
from models import FPSCounter, rand_map, has_tree, save_highscore

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GROUND = 60
JUMP_SPEED = 10
MOVEMENT_SPEED = 10

maps = list(reversed(open('map_s.txt').read().splitlines()))
map1 = list(reversed(open('map_0.txt').read().splitlines()))
map2 = list(reversed(open('map_1.txt').read().splitlines()))
map3 = list(reversed(open('map_2.txt').read().splitlines()))
map4 = list(reversed(open('map_3.txt').read().splitlines()))
platform = list(map(lambda x, y: x+y, maps, map2))

list_map = [map1, map2, map3, map4]


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='SKE Jump (Demo)')

        self.BG = arcade.Sprite(filename='images/backgroundForest.png',
                                center_x=SCREEN_WIDTH//2,
                                center_y=SCREEN_HEIGHT//2)

        self.player = Player('images/SKE_N.png')

        self.map = Map()

        self.physics = physics.PhysicsEnginePlatformer(self.player,
                                                       self.map)

        self.score = 0

        self.write_score = False

        self.starter = False

        self.game_state = 'freeze'

        self.fps = FPSCounter()

    def change_game_state(self, key=None):
        if self.player.is_dead:
            if not self.write_score:
                save_highscore(str(self.score))
                self.write_score = True

            self.game_state = 'dead'

            if key == arcade.key.R:
                self.score = 0

                self.write_score = False

                self.player.center_x = 100
                self.player.center_y = GROUND

                self.player.is_dead = False

                global platform
                platform = list(map(lambda x, y: x+y, maps, map2))

                self.map.sprite_list = []
                self.map.generate_map()

                self.game_state = 'freeze'
            
            if key == arcade.key.ESCAPE:
                arcade.close_window()
        
        if self.game_state == 'freeze':
            if key == arcade.key.SPACE:
                self.game_state = 'running'
                
    def dead_draw(self):
        if self.game_state == 'dead':

            high_score = open('score.txt').read()

            arcade.draw_text(f'Your score : {self.score}\nHigh score : {int(high_score)}\nPress "R" to restart\nPress "ESC" to exit',
                         self.width//2 - 180, self.height//2 - 80,
                         arcade.color.BLACK, 40)

    def draw_start(self):
        if self.game_state == 'freeze':
            arcade.draw_text(f' Press "Space bar"\n to start and Jump',
                         self.width//2 - 200, self.height//2,
                         arcade.color.BLACK, 40)

    def update(self, delta):
        self.physics.tree_hit()
        self.player.update()
        self.change_game_state()

        if not self.player.is_dead and self.game_state == 'running':
            self.score += 1
            self.physics.update()
            self.map.update_animation()
            self.map.check_end_map()
        

    def on_draw(self):
        arcade.start_render()

        self.change_game_state()

        self.BG.draw()

        self.player.draw()

        self.map.draw()

        arcade.draw_text(str(self.score),
                         self.width//2, self.height - 40,
                         arcade.color.WHITE, 30)

        self.fps.tick()

        arcade.draw_text(f'fps {self.fps.get_fps():.0f} ms',
                         SCREEN_WIDTH - 70, SCREEN_HEIGHT - 20,
                         arcade.color.RED, 10)
        
        self.dead_draw()

        self.draw_start()

    def on_key_press(self, key, key_modifiers):
        self.change_game_state(key)
        if key == arcade.key.SPACE:
            if self.physics.can_jump():
                self.player.change_y = JUMP_SPEED



class Player(arcade.Sprite):
    def __init__(self, file_name):
        super().__init__(filename=file_name, scale=0.5)

        # Create SKE normal state at textures index 0
        self.ske_n = arcade.load_texture(file_name)
        self.textures.append(self.ske_n)

        self.center_x = 100
        self.center_y = GROUND

        self.is_dead = False

    def update(self):
        self.fall()

    def fall(self):
        if self.center_y < 50:
            self.is_dead = True


class TreeSprite(arcade.Sprite):
    NUM = 0
    def __init__(self, file_name, model_x=600,
                 model_y=GROUND, end_map=False):
        super().__init__(filename=file_name, scale=0.25,
                         center_x=model_x, center_y=model_y)

        self.end_map = end_map
        self.is_tree = True
        TreeSprite.NUM += 1
        self.num = TreeSprite.NUM

    def update_animation(self):
        self.center_x -= MOVEMENT_SPEED

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
                    if has_tree():
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
                    if has_tree():
                        self.append(TreeSprite('images/treePineFrozen.png',
                                            790 + j * 20,
                                            10 + i * 20))


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
