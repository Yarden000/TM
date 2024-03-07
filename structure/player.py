import pygame, sys
from settings import *
from entities import Entity


class Player(Entity):
    def __init__(self):
        super().__init__((WIDTH/2,HEIGHT/2), '../graphics/test/player.png')
        self.speed = 5

    def move(self):
        
        self.keys = pygame.key.get_pressed()
        self.direction = VEC_2()
        self.direction.x = 0
        self.direction.y = 0
        if self.keys[pygame.K_w]:
            self.direction.y += -1
        if self.keys[pygame.K_s]:
            self.direction.y += 1
        if self.keys[pygame.K_d]:
            self.direction.x += 1
        if self.keys[pygame.K_a]:
            self.direction.x += -1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.movement = self.direction * self.speed

        """
        comment changer player_displacement pour que tous les fichiers le voient?
        """
        player_displacement -= self.movement
        self.pos += self.movement

    def display(self):
        self.screen.blit(self.image, self.image.get_rect(center = (WIDTH/2, HEIGHT/2)))

    def run(self):
        self.move()