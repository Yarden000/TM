'''main file'''
import sys
import pygame
from settings import (
    WIDTH,
    HEIGHT,
    FPS, 
    angle_between_vectors_plus_minus_pi,
    VEC_2
)
from compiler import (
    Compiler,
    # CompilerForTestingMapGen
    )
from input import InputManager


class Game:
    '''game class'''
    def __init__(self) -> None:
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        flags =  pygame.DOUBLEBUF| pygame.HWSURFACE  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, 16)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.set_alpha(None)

        # test
        WIDTH_, HEIGHT_ = pygame.display.get_window_size()
        # print(WIDTH_, HEIGHT_)

        pygame.display.set_caption('Survivorio')

        self.input_manager = InputManager()
        self.clock = pygame.time.Clock()
        self.compiler = Compiler(self.input_manager)
        # self.compiler_for_testing_map_gen = CompilerForTestingMapGen()   # enable this and dissable compiler to test map gen

    def run(self) -> None:
        '''runs the game'''
        game_run = True
        while game_run:
            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT or self.input_manager.quit():  # checks if quit
                    pygame.quit()
                    sys.exit()

            fps = self.input_manager.speed_up_fps(FPS)
            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.compiler.run(dt)
            self.clock.tick(fps)  # should be FPS
            # (self.clock.get_fps())

            # testing
            pos = pygame.mouse.get_pos()
            angle = angle_between_vectors_plus_minus_pi(VEC_2(1, 0), VEC_2(pos) - VEC_2(WIDTH / 2, HEIGHT / 2))
            print(angle)
            


if __name__ == '__main__':  # checks if it is the main file
    game = Game()
    game.run()
