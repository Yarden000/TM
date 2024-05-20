import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2
    )
from entities import Entity


class Player(Entity):
    def __init__(self):
        super().__init__((WIDTH/2,HEIGHT/2))
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/player.png'), (self.size, self.size))
        self.speed = 100

    def move(self, dt, camera):
        
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

        displacement = self.movement * dt

        camera.player_displacement -= displacement
        camera.true_player_displacement -= displacement
        self.pos += displacement
        
    def display(self, screen, camera):
        screen.blit(self.image, self.image.get_rect(center = (WIDTH/2, HEIGHT/2)))

    def run(self, dt, camera):
        self.move(dt, camera)