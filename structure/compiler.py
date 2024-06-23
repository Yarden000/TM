import pygame, sys
from map import (Map, 
    MapGenerator_testing
    )
from entities import (
    EntityManager, 
    Entity, 
    Player, 
    Ressource, 
    Animal
    )
from spawner import (
    Spawner
)
from camera import Camera


class Compiler:
    '''
    all the playable part of the game
    '''
    
    def __init__(self, input_manager):
        self.outside_range_enteties = []
        self.input_manager = input_manager
        self.camera = Camera()
        self.map = Map()
        self.entity_manager = EntityManager(self.input_manager, self.camera) # camera is for testing
        self.displayer = Displayer(self.map, self.camera, self.entity_manager)
        self.spawner = Spawner(self.camera, self.map, self.entity_manager)
    
    def run(self, dt):
        # all the interactions / events / calculations of the game
        self.entity_manager.run(dt)

        # test
        self.spawner.spawn_ent_v2(dt, Animal)
        self.spawner.spawn_ent_v2(dt, Ressource)

        self.displayer.run()
        


class Displayer:
    # il faut ajouter une fonction qui verifie si un element est dans la window avant de le display

    def __init__(self, map, camera, entity_manager):
        self.screen = pygame.display.get_surface()
        self.map = map
        self.camera = camera
        self.entity_manager = entity_manager

    def run(self):
        self.screen.fill('blue')               
        self.map.display(self.camera)


        for i in self.entity_manager.entity_list:
            # trier selon la position
            i.display(self.screen, self.camera)
            i.hitbox.draw(self.screen, self.camera) 
        #print(len(self.displayable_entenies))
        # for debugging:
        #self.entity_manager.draw_regions(self.camera.player_displacement)
        pygame.display.update()



class Compiler_for_testing_map_gen:
    
    def __init__(self, input_manager):
        # to test the map gen, need to dissable the run funcion
        self.maptest = MapGenerator_testing(4, 3, base_grid_size = 1, octaves = 5, persistence = 0.85, frequency = 2, random_prob = 0.2)
        self.maptest.display_biomes()
        #self.maptest.display_strengths()
        pygame.display.update()