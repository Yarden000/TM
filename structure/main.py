import pygame, sys
from settings import *
from compiler import Compiler



class Displayer:
    # il faut ajouter une fonction qui verifie si un element est dans la window avant de le display

    def __init__(self):
        self.screen = pygame.display.get_surface()

    def run(self):
        self.screen.fill('blue')               #pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | Enemy count: {len(Enemie.instances)}")
        
        for i in displayable_entenies:
            # trier selon la position
            i.display()
        
        
        pygame.display.update()




class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survivorio')

        self.clock = pygame.time.Clock()

        self.compiler = Compiler()
        self.displayer = Displayer()


    def run(self):
        game_run = True
        while game_run:

            for event in pygame.event.get():# event loop
                if event.type == pygame.QUIT:# checks if quit
                    pygame.quit()
                    sys.exit()   


            self.compiler.run()
            self.displayer.run()

            self.clock.tick(FPS)


if __name__ == '__main__':# checks if it is the main file
    game = Game()
    game.run()