import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    FPS, 
    )  # map_grid ne veut pas fonctionner
from compiler import Compiler
from map import MapGenerator_testing, MapGenerator



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

            for event in pygame.event.get():# event loop
                if event.type == pygame.QUIT:# checks if quit
                    pygame.quit()
                    sys.exit()   

            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))}")

            self.compiler.run()

            #self.clock.tick(1000)
            self.clock.tick(FPS)


if __name__ == '__main__':# checks if it is the main file
    game = Game()
    game.run()