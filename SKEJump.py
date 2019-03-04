import arcade
from models import World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.SKE = SKE(self.world.ske, 'images/SKE_N.png')

    def update(self, delta):
        pass
    
    def on_draw(self):
        arcade.start_render()

        self.SKE.draw()

        arcade.draw_text(str(self.world.score),
                            self.width//2, self.height - 40,
                            arcade.color.WHITE, 30)


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


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()