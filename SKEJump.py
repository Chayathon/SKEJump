import arcade
from models import World, GROUND

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='SKE Jump (Demo)')

        self.BG = arcade.load_texture('images/backgroundForest.png')

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.SKE = SKE(self.world.ske, 'images/SKE_N.png')

        self.barrier = BarrierSprite(self.world.barrier, 'images/treePineFrozen.png')

    def hits(self):
        if arcade.check_for_collision(self.SKE, self.barrier):
            self.world.ske.is_dead = True

    def update(self, delta):

        self.hits()

        if not self.world.ske.is_dead:
            self.world.update(delta)
            self.SKE.update()
            self.barrier.update()
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      texture=self.BG)

        self.SKE.draw()

        self.barrier.draw()


        arcade.draw_rectangle_filled(SCREEN_WIDTH//2, 50, 
                                    SCREEN_WIDTH, 100, 
                                    arcade.color.SNOW)


        arcade.draw_text(str(self.world.score),
                            self.width//2, self.height - 40,
                            arcade.color.WHITE, 30)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)


class SKE(arcade.Sprite):
    def __init__(self, model, file_name):
        super().__init__(filename=file_name)

        # Create SKE normal state at textures index 0
        self.ske_n = arcade.load_texture(file_name)
        self.textures.append(self.ske_n)

        self.status = 0
        self.model = model
        self.center_x = self.model.x
        self.center_y = self.model.y

        self.change_angle = 1
    
    def update(self):
        self.center_x = self.model.x
        self.center_y = self.model.y

        if self.model.y == GROUND and self.angle == 0.0:
            pass

        elif self.model.y == GROUND and self.angle != 0.0:
            self.angle += self.change_angle

        else:
            self.angle -= self.change_angle
        

class BarrierSprite(arcade.Sprite):
    def __init__(self, model, file_name):
        super().__init__(filename=file_name, scale=0.5)

        self.model = model
        self.center_x = self.model.x
        self.center_y = self.model.y
    
    def update(self):
        self.center_x = self.model.x
        self.center_y = self.model.y


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()