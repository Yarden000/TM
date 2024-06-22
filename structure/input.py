import pygame, sys, time
from settings import(
    VEC_2
)

class Input_manager:
    def __init__(self):
        pass

    def player_movement(self):
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            return 100 * fps
        return fps
    
    def attack_click(self):  # testing
        if pygame.mouse.get_pressed()[0]:
            return pygame.mouse.get_pos()
        return None