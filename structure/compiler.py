import pygame, sys
from map import Map
from settings import *
from player import Player
from entities import Entity


class Compiler:
    
    def __init__(self):
        self.spawn_player()

        # test
        self.test_entity = Entity()

    def spawn_player(self):
        self.player = Player()

    def run(self):

        # all the interactions / events / calculations of the game
        self.player.run()