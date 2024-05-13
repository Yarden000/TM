import pygame
import sys
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
)
from compiler import Compiler


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survivorio')

        self.clock = pygame.time.Clock()

        self.compiler = Compiler()

    def run(self):
        game_run = True
        while game_run:
            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:  # checks if quit
                    pygame.quit()
                    sys.exit()

            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.compiler.run(dt)
            #self.clock.tick(1000)
            self.clock.tick(FPS)


if __name__ == '__main__':  # checks if it is the main file
    game = Game()
    game.run()
