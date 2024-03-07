import pygame, sys
from settings import *
from enteties import Entety


class Player(Entety):
    def __init__(self):
        super().__init__()
        self.pos = VEC_2(200,200)

    def run(self):
        pass