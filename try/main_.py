# hello

import pygame, sys
from settings_TM import *
from Map import Map
from player import Player


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Survivorio')
        self.clock = pygame.time.Clock()

        #self.player = Player()
        #self.map = Map()

        
           

    def run(self):
        game_run = True
        while game_run:
            for event in pygame.event.get():# event loop
                if event.type == pygame.QUIT:# checks if quit
                    pygame.quit()
                    sys.exit()

            #pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | Enemy count: {len(Enemie.instances)}")
            self.screen.fill('blue')
            #get_P_direction(player_displacement) # updetes the player displacement

            #self.map.run()
            #self.player.run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':# checks if it is the main file
    game = Game()
    game.run()