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


WIDTH, HEIGHT = 800, 800
FPS = 60

VEC_2 = pygame.Vector2
VEC_3 = pygame.Vector3
dot = lambda v1, v2: pygame.math.Vector2.dot(v1, v2)

displayable_entenies = []  # need to add a way of ordering from clostest to farthest
map_size = 100 # size of the map_grid / number of cells
map_grid = {}
cell_size = 100
biome_types = [{'name': 'desert', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/desert.png'), (cell_size, cell_size))}, 
               {'name': 'plains', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/plains.png'), (cell_size, cell_size))}, 
               {'name': 'forest', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/forest.png'), (cell_size, cell_size))}]


