import pygame, sys
from map import Map
from settings import *
from player import Player
from entities import Entity
from camera import Camera


class Compiler:
    
    def __init__(self):
        self.camera = Camera()
        self.player = Player(self.camera)

        # test
        self.test_entity = Entity(self.camera)

        

    def run(self):

        # all the interactions / events / calculations of the game
        self.player.run()