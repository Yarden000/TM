import pygame, sys
from map import Map
from settings import *
from player import Player


class Compiler:
    
    def __init__(self):
        self.spawn_player()

    def spawn_player(self):
        self.player = Player()

    def run(self):

        # all the interactions / events / calculations of the game
        self.player.run()