import pygame, sys
from map import Map
from player import Player
from entities import Entity
from camera import Camera


class Compiler:
    
    def __init__(self):
        self.displayable_entenies = []  # need to add a way of ordering from clostest to farthest

        self.camera = Camera()
        self.player = Player(self.displayable_entenies)
        self.map = Map()

        self.displayer = Displayer(self.map, self.camera, self.displayable_entenies)

        # test
        self.test_entity = Entity(self.displayable_entenies, size = 200)

        

    def run(self):

        # all the interactions / events / calculations of the game
        self.player.run(self.camera)

        self.displayer.run()


class Displayer:
    # il faut ajouter une fonction qui verifie si un element est dans la window avant de le display

    def __init__(self, map, camera, displayable_entenies):
        self.screen = pygame.display.get_surface()
        self.map = map
        self.camera = camera
        self.displayable_entenies = displayable_entenies

    def run(self):
        self.screen.fill('blue')               
        self.map.display(self.camera)
        for i in self.displayable_entenies:
            # trier selon la position
            i.display(self.camera)
        pygame.display.update()