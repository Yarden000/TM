'''comèiler and displayer'''
import pygame
import pymunk
from map import (
    Map,
    MapGeneratorTesting
    )
from entities import (
    Entity,
    EntityManager,
    Ressource,
    Animal
    )
from spawner import (
    Spawner
)
from camera import Camera
import behaviors


class Compiler:
    '''
    all the playable part of the game
    '''

    def __init__(self, input_manager) -> None:
        self.outside_range_enteties: list[Entity] = []
        self.input_manager = input_manager
        self.camera = Camera()
        self.map = Map()
        self.entity_manager = EntityManager(self.input_manager, self.camera)  # camera is for testing
        self.displayer = Displayer(self.map, self.camera, self.entity_manager)
        self.spawner = Spawner(self.camera, self.map, self.entity_manager)

    def run(self, dt) -> None:
        '''all the interactions / events / calculations of the game'''
        self.entity_manager.run(dt)

        self.spawner.spawn_ent_v2(dt, Animal)
        self.spawner.spawn_ent_v2(dt, Ressource)


        self.displayer.run()


class Displayer:
    '''
    responsible for displaing all the elements whilst the game is running
    and ordering background-forground
    '''
    # il faut ajouter une fonction qui verifie si un element est dans la window avant de le display

    def __init__(self, terrain, camera, entity_manager) -> None:
        self.screen = pygame.display.get_surface()
        self.terrain = terrain
        self.camera = camera
        self.entity_manager = entity_manager

    def run(self) -> None:
        '''displays'''
        self.screen.fill('blue')
        self.terrain.display(self.camera)

        displacement = self.camera.player_displacement
        for i in self.entity_manager.entity_list:
            # trier selon la position
            i.display(self.screen, self.camera.player_displacement)

        for thing in behaviors.visuals:
            thing.draw(self.screen, self.camera.player_displacement)
        behaviors.visuals = []
            

        # self.entity_manager.player.visualise_directions(self.screen)
        # print(len(self.displayable_entenies))
        # for debugging:
        self.entity_manager.draw_regions(self.camera.player_displacement)

        pygame.display.update()


class CompilerForTestingMapGen:
    '''calculates and visualises the map gen'''
    def __init__(self) -> None:
        # to test the map gen, need to dissable the run funcion
        self.maptest = MapGeneratorTesting(4, 3, 1, 5, 0.85, 2, 0.2)
        self.maptest.display_biomes()
        # self.maptest.display_strengths()
        pygame.display.update()
