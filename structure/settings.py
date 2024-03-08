#   https://www.youtube.com/watch?v=T9vYgZJCmeI

import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surf, 'Black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)

def int_VEC(vector):
    return VEC_2(int(vector.x), int(vector.y))


WIDTH, HEIGHT = 600, 600
FPS = 60

VEC_2 = pygame.Vector2
VEC_3 = pygame.Vector3

displayable_entenies = []  # need to add a way of ordering from clostest to farthest


