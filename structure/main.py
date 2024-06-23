import pygame
import sys
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    VEC_2
)
from compiler import (
    Compiler, 
    Compiler_for_testing_map_gen
    )
from input import Input_manager
# testing
from collisions import Collision_detector

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survivorio')

        self.input_manager = Input_manager()
        self.clock = pygame.time.Clock()
        self.compiler = Compiler(self.input_manager)
        #self.compiler_for_testing_map_gen = Compiler_for_testing_map_gen()   # enable this and dissable compiler to test map gen
        self.collision_detector = Collision_detector()

    def run(self):
        game_run = True
        while game_run:
            # testing
            #print(self.collision_detector.Rect_Circle({'pos': (2, 2), 'r': 1}, {'pos': (0, 0), 'vec1': VEC_2(1, 1), 'vec2': VEC_2(-1, 1)}))
            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:  # checks if quit
                    pygame.quit()
                    sys.exit()

            # testing
            self.keys = pygame.key.get_pressed()
            fps = self.input_manager.speed_up_fps(FPS)


            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.compiler.run(dt)
            self.clock.tick(fps)  # should be FPS


if __name__ == '__main__':  # checks if it is the main file
    game = Game()
    game.run()
