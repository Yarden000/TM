#   https://www.youtube.com/watch?v=T9vYgZJCmeI

import pygame


def debug(info, y = 10, x = 10):  # why not work?
    font = pygame.font.Font(None, 30)
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surf, 'Black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)


WIDTH, HEIGHT = 800, 800
FPS = 60

VEC_2 = pygame.Vector2
VEC_3 = pygame.Vector3



