import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2
    )


class Camera:

    def __init__(self):
        self.player_displacement = VEC_2(WIDTH/2, HEIGHT/2)
        self.true_player_displacement = VEC_2()
