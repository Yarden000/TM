import pygame, sys
from map import Map
from settings import *

# hello
class Displayer:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survivorio')

    def run(self):
        self.screen.fill('blue')               #pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | Enemy count: {len(Enemie.instances)}")
        
        for i in displayable_entenies:
            i.display()
        
        
        pygame.display.update()




class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.Displayer = Displayer()

        

    def run(self):
        game_run = True
        while game_run:

            for event in pygame.event.get():# event loop
                if event.type == pygame.QUIT:# checks if quit
                    pygame.quit()
                    sys.exit()   

            self.Displayer.run()

            self.clock.tick(FPS)


if __name__ == '__main__':# checks if it is the main file
    game = Game()
    game.run()