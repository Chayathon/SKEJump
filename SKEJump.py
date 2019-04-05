import arcade
import time, collections
from models import World, GROUND

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


map = list(reversed(open('map_1.txt').read().splitlines()))

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

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='SKE Jump (Demo)')

        self.BG = arcade.Sprite(filename='images/backgroundForest.png',
                                center_x=SCREEN_WIDTH//2,
                                center_y=SCREEN_HEIGHT//2)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.SKE = SKE(self.world.ske, 'images/SKE_N.png')

        self.map = Map()

        self.barrier = BarrierSprite(self.world.barrier, 'images/treePineFrozen.png')

        # self.platform = arcade.SpriteList()
        # self.platform = arcade.Sprite(filename='images/slice01.png',
        #                                 )

        self.fps = FPSCounter()

        self.position = []

        # self.generate_map()
        

    def change_view(self):
        arcade.set_viewport(self.SKE.center_x - 200,
                            self.SKE.center_x - 200 + SCREEN_WIDTH,
                            0, SCREEN_HEIGHT)

    def hits(self):
        if arcade.check_for_collision(self.SKE, self.barrier):
            self.world.ske.is_dead = True

    # def generate_map(self):
    #     self.platform_x = 35
    #     self.platform_y = 35

    #     for i in map:
    #         for j in i:

    #             if j == 'P':

    #                 self.platform.append(arcade.Sprite('images/slice01.png',
    #                                                     center_x=self.platform_x,
    #                                                     center_y=self.platform_y))
                    

    #             elif j == '0':
    #                 # self.platform = arcade.SpriteList('images/slice33.png', 
    #                 #                               center_x=self.platform_x, 
    #                 #                               center_y=self.platform_y)

    #                 self.platform.append(arcade.Sprite('images/slice33.png',
    #                                                     center_x=self.platform_x,
    #                                                     center_y=self.platform_y))
                

    #             self.platform_x += 70
    #         self.platform_y += 70
            
    #         # self.platform.draw()

    # def generate_map(self):
    #     for i in range(len(map)):
    #         for j in range(len(map[i])):
    #             if map[i][j] == 'P':
    #                 self.position.append([j, i])
    #     print(self.position)

    # def draw_map(self):
        
    #     box = arcade.Sprite('images/treePineFrozen.png', center_x=SCREEN_WIDTH//2, center_y=100, scale=10)
    #     # for position in self.position:
    #     #     box.set_position(int(position[0]) , int(position[1]))
    #     box.draw()



    def update(self, delta):

        self.BG.draw()
        self.hits()

        

        if not self.world.ske.is_dead:
            self.world.update(delta)
            self.SKE.update()
            self.barrier.update()

            self.change_view()
            from models import MOVEMENT_SPEED
            self.BG.center_x += MOVEMENT_SPEED
        
            print(self.fps.get_fps())
        
        # self.draw_map()
    
    
    def on_draw(self):
        arcade.start_render()

        # arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
        #                               SCREEN_WIDTH, SCREEN_HEIGHT,
        #                               texture=self.BG)

        self.BG.draw()

        self.SKE.draw()

        self.barrier.draw()

        self.map.draw()


        # arcade.draw_rectangle_filled(SCREEN_WIDTH//2, 50, 
        #                             SCREEN_WIDTH, 100, 
        #                             arcade.color.SNOW)

        

        # arcade.draw_text(str(self.world.score),
        #                     self.width//2, self.height - 40,
        #                     arcade.color.WHITE, 30)
        self.fps.tick()

        # self.generate_map()

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


class Map(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.generate_map()


    def generate_map(self):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 'P':
                    self.append(arcade.Sprite('images/slice01.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))

                elif map[i][j] == '0':
                    self.append(arcade.Sprite('images/slice33.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))

                elif map[i][j] == 'U':
                    self.append(arcade.Sprite('images/slice07.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))

                elif map[i][j] == 'D':
                    self.append(arcade.Sprite('images/slice06.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))
                
                elif map[i][j] == 'u':
                    self.append(arcade.Sprite('images/slice18.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))

                elif map[i][j] == 'd':
                    self.append(arcade.Sprite('images/slice17.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))
                
                elif map[i][j] == 'T':
                    self.append(arcade.Sprite('images/slice21.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))

                elif map[i][j] == 'B':
                    self.append(arcade.Sprite('images/slice22.png', 
                                              center_x= 35 + j * 70,
                                              center_y= 35 + i * 70))

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()