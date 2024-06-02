import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2
    )
from entities import Entity


class Player(Entity):
    movable = True
    def __init__(self, camera):
        super().__init__((0, 0))
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/player.png'), (self.size, self.size))
        self.speed = 100
        self.camera = camera

    def move(self, displacement):
        self.camera.player_displacement -= displacement
        self.camera.true_player_displacement -= displacement
        self.hitbox.pos += displacement

    def display(self, screen, camera):
        screen.blit(self.image, self.image.get_rect(center = (WIDTH/2, HEIGHT/2)))

    def run(self, dt):
        pass