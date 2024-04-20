import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2
    )
from entities import Entity


class Player(Entity):
    def __init__(self, displayable_entenies):
        super().__init__((WIDTH/2,HEIGHT/2), 64, '../graphics/test/player.png')
        displayable_entenies.append(self)
        self.speed = 2

    def move(self, camera):
        
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
        if self.keys[pygame.K_c]:
            self.movement = self.direction * self.speed * 10
        else:
            self.movement = self.direction * self.speed

        camera.player_displacement -= self.movement
        self.pos += self.movement

    def display(self, camera):
        self.screen.blit(self.image, self.image.get_rect(center = (WIDTH/2, HEIGHT/2)))

    def run(self, camera):
        self.move(camera)