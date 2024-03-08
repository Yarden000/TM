import pygame, sys
from settings import *


class Camera:

    def __init__(self):
        self.player_displacement = VEC_2(WIDTH/2, HEIGHT/2)
