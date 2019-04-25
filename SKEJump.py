import arcade
from random import randint
from models import FPSCounter

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GROUND = 175
MOVEMENT_SPEED = 10

map = list(reversed(open('map_0.txt').read().splitlines()))


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='SKE Jump (Demo)')

        self.BG = arcade.Sprite(filename='images/backgroundForest.png',
                                center_x=SCREEN_WIDTH//2,
                                center_y=SCREEN_HEIGHT//2)

        # self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.player = Player('images/SKE_N.png')

        self.map = Map()

        self.tree = TreeSprite('images/treePineFrozen.png')

        self.platform = arcade.PhysicsEnginePlatformer(self.player, 
                                                       self.map)

        self.fps = FPSCounter()

    def hits(self):
        if arcade.check_for_collision(self.player, self.tree):
            self.player.is_dead = True

    def update(self, delta):
        self.BG.draw()
        self.hits()

        if not self.player.is_dead:
            self.player.update()
            self.tree.update()
            self.platform.update()
            self.map.update_animation()
    
    def on_draw(self):
        arcade.start_render()

        self.BG.draw()

        self.player.draw()

        self.tree.draw()

        self.map.draw()

        # arcade.draw_text(str(self.world.score),
        #                     self.width//2, self.height - 40,
        #                     arcade.color.WHITE, 30)

        self.fps.tick()

        arcade.draw_text(f'fps {self.fps.get_fps():.0f} ms',
                        SCREEN_WIDTH - 70, SCREEN_HEIGHT - 20,
                        arcade.color.RED, 10)

    def on_key_press(self, key, key_modifiers):
        # self.world.on_key_press(key, key_modifiers)
        pass


class Player(arcade.Sprite):
    def __init__(self, file_name):
        super().__init__(filename=file_name)

        # Create SKE normal state at textures index 0
        self.ske_n = arcade.load_texture(file_name)
        self.textures.append(self.ske_n)

        self.status = 0
        self.center_x = 100
        self.center_y = GROUND

        self.change_angle = 1

        self.is_dead = False

    def update(self):
        self.center_x += 0
        self.center_y += 0
        

class TreeSprite(arcade.Sprite):
    def __init__(self, file_name):
        super().__init__(filename=file_name, scale=0.3)

        self.center_x = 600
        self.center_y = GROUND
    
    def update(self):
        self.center_x -= MOVEMENT_SPEED

        if self.center_x < -30:
            self.center_x = randint(SCREEN_WIDTH + 20, 
                                    SCREEN_WIDTH + 100)
            
            self.center_y = GROUND


class Block(arcade.Sprite):
    def __init__(self, file_name, model_x, model_y):
        super().__init__(filename=file_name,
                         center_x=model_x, 
                         center_y=model_y)

    def update_animation(self):
        self.center_x -= MOVEMENT_SPEED

        if self.center_x < (-70):
            # self.kill()
            self.center_x = 1230


class Map(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.generate_map()

    def generate_map(self):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 'P':
                    self.append(Block('images/slice01.png', 
                                    35 + j * 70,
                                    35 + i * 70))

                elif map[i][j] == '0':
                    self.append(Block('images/slice33.png', 
                                    35 + j * 70,
                                    35 + i * 70))

                elif map[i][j] == 'U':
                    self.append(Block('images/slice07.png', 
                                    35 + j * 70,
                                    35 + i * 70))

                elif map[i][j] == 'D':
                    self.append(Block('images/slice06.png', 
                                    35 + j * 70,
                                    35 + i * 70))
                
                elif map[i][j] == 'u':
                    self.append(Block('images/slice18.png', 
                                    35 + j * 70,
                                    35 + i * 70))

                elif map[i][j] == 'd':
                    self.append(Block('images/slice17.png', 
                                    35 + j * 70,
                                    35 + i * 70))
                
                elif map[i][j] == 'T':
                    self.append(Block('images/slice21.png', 
                                    35 + j * 70,
                                    35 + i * 70))

                elif map[i][j] == 'B':
                    self.append(Block('images/slice22.png', 
                                    35 + j * 70,
                                    35 + i * 70))


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()