'''https://www.youtube.com/watch?v=T9vYgZJCmeI'''
import math
import pygame


def debug(info, y=10, x=10):
    '''displays text on screen'''
    font = pygame.font.Font(None, 30)
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surf, 'Black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)


WIDTH, HEIGHT = 800, 800
FPS = 60

VEC_2 = pygame.Vector2
VEC_3 = pygame.Vector3


def angle_between_vectors(v1, v2):
    '''inn radients'''
    if v1.magnitude() == 0 or v2.magnitude() == 0:
        raise ValueError('Null Vector')
    sign = -1 if v1.cross(v2) > 0 else 1
    return math.acos(v1.dot(v2) / (v1.magnitude() * v2.magnitude())) * sign
