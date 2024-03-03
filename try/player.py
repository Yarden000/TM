import pygame, sys
from settings_TM import *
from debug_TM import debug

class Player:

    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.pos = VEC(WIDTH/2, HEIGHT/2)
        self.image = pygame.image.load('C:/Users/yarde/OneDrive/Desktop/Yarden/Survival_game/simeon_et _yarden/graphics/wizard.png').convert_alpha()
        self.rect = self.image.get_rect(center = self.pos)
        self.speed = 5
        self.render_dist = 500


    def draw(self):
        self.display_surf.blit(self.image, self.rect)

    
    def run(self):
        self.draw()

