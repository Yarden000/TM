'''
handels the inputs and at what point in the gamewhat imput should do
for exampel a clic normaly is an attack, but whebn the player is in the inventory
it could mean to select an item
'''
import pygame, pymunk
from settings import (
    VEC_2
)


class InputManager:
    '''manages the inputs'''
    def __init__(self) -> None:
        pass

    def quit(self) -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            return True
        return False

    def player_movement(self) -> pymunk.Vec2d:
        '''whitch direction teh player is moving'''
        keys = pygame.key.get_pressed()
        direction = pymunk.Vec2d(0, 0)
        if keys[pygame.K_w]:
            direction += pymunk.Vec2d(0, -1)
        if keys[pygame.K_s]:
            direction += pymunk.Vec2d(0, 1)
        if keys[pygame.K_d]:
            direction += pymunk.Vec2d(1, 0)
        if keys[pygame.K_a]:
            direction += pymunk.Vec2d(-1, 0)
        if direction.length != 0:
            direction = direction.normalized()
        if keys[pygame.K_c]:
            movement = direction * 50
        else:
            movement = direction

        return movement

    def speed_up_fps(self, fps) -> int:
        '''to see the max fps'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            return 100 * fps
        return fps

    def attack_click(self) -> tuple[int,int] | None:
        '''testing'''
        if pygame.mouse.get_pressed()[0]:
            return pygame.mouse.get_pos()
        return None
