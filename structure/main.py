import pygame, sys
import settings
#from settings import *     why doesn't it work? Probleme avec les variables globales et le *
from compiler import Compiler
from map import MapGenerator_testing, MapGenerator



class Displayer:
    # il faut ajouter une fonction qui verifie si un element est dans la window avant de le display

    def __init__(self, map):
        self.screen = pygame.display.get_surface()
        self.map = map

    def run(self):
        self.screen.fill('blue')               
        self.map.display()
        for i in settings.displayable_entenies:
            # trier selon la position
            i.display()
        pygame.display.update()




class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption('Survivorio')

        self.clock = pygame.time.Clock()

        self.map_gen = MapGenerator(settings.biome_types, 3, 6, 0.5, 2, 0.3) #(biome_types, base_gris_size, octaves, persistence, frequency, random)
        self.time = pygame.time.get_ticks()
        settings.map_grid = self.map_gen.make_map()
        self.time = pygame.time.get_ticks() - self.time
        print('time =', self.time / 1000)

        self.compiler = Compiler()
        self.displayer = Displayer(self.compiler.map)

        '''
        # to test and visualise the map generation, for finetuning the parameters
        self.test_map = MapGenerator_testing(3, 5, 1, 4, 0.5, 2, 0) #(biome_number, pixel_sise, base_gris_size, octaves, persistence, frequency, random)
        #self.test_map.display_strengths(self.test_map.perlin_noise())
        self.test_map.display_biomes(self.test_map.simple_superposition())
        pygame.display.update()
        '''


    def run(self):
        game_run = True
        while game_run:

            for event in pygame.event.get():# event loop
                if event.type == pygame.QUIT:# checks if quit
                    pygame.quit()
                    sys.exit()   

            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))}")

            self.compiler.run()
            self.displayer.run()

            #self.clock.tick(1000)
            self.clock.tick(settings.FPS)


if __name__ == '__main__':# checks if it is the main file
    game = Game()
    game.run()