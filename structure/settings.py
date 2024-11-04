'''https://www.youtube.com/watch?v=T9vYgZJCmeI'''
import math
import pygame, pymunk


def debug(info, y=10, x=10) -> None:
    '''displays text on screen'''
    font = pygame.font.Font(None, 30)
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surf, 'Black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)

debug_info:list[tuple[str, float, float]] = []


WIDTH, HEIGHT = 1000, 800
FPS = 1200
PI = math.pi

VEC_2 = pygame.Vector2
VEC_3 = pygame.Vector3
PY_VEC_2 = pymunk.Vec2d
def convert_to_pymunk(vec):
    return pymunk.Vec2d(vec.x, vec.y)


def angle_between_vectors_0_to_2pi(v1: VEC_2, v2: VEC_2) -> float:
    '''in radients, from 0 to 2pi'''
    if v1.length == 0 or v2.length == 0:
        raise ValueError('Null Vector')
    tmp_angle =  math.acos(v1.dot(v2) / (v1.length * v2.length))
    if v1.cross(v2) > 0:
        angle = 2 * math.pi - tmp_angle
    else:
        angle = tmp_angle
    return angle

def angle_between_vectors_plus_minus_pi(v1: VEC_2, v2: VEC_2) -> float:
    '''in radients, from pi to -pi'''
    if v1.length == 0 or v2.length == 0:
        raise ValueError('Null Vector')

    perp_v1 = VEC_2(v1.y, -v1.x)
    angle =  math.acos(v1.dot(v2) / (v1.length * v2.length))
    if v2.dot(perp_v1) < 0:
        return -angle
    return angle

    

