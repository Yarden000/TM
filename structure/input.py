'''
handels the inputs and at what point in the gamewhat imput should do
for exampel a clic normaly is an attack, but whebn the player is in the inventory
it could mean to select an item
'''
import pygame
from settings import(
    VEC_2
)

class InputManager:
    '''manages the inputs'''
    def __init__(self):
        pass

    def player_movement(self):
        '''whitch direction teh player is moving'''
        keys = pygame.key.get_pressed()
        direction = VEC_2()
        if keys[pygame.K_w]:
            direction.y += -1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_a]:
            direction.x += -1
        if direction.magnitude() != 0:
            direction = direction.normalize()
        if keys[pygame.K_c]:
            movement = direction * 10
        else:
            movement = direction

        return movement


    def speed_up_fps(self, fps):
        '''to see the max fps'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            return 100 * fps
        return fps

    def attack_click(self):
        '''testing'''
        if pygame.mouse.get_pressed()[0]:
            return pygame.mouse.get_pos()
        return None
