import pygame


WIDTH = 1420
HEIGHT = 780 - 200
FPS = 60


VEC = pygame.math.Vector2


tile_size = 10
map_size = (30, 30) #tiles

def MAP_grid():
    map_grid = {}
    for i in range(-map_size[0], map_size[0]):
        for j in range(-map_size[1], map_size[1]):
            map_grid[(i, j)] = {'pos': (i, j), 'time': 0}
    return map_grid

MAP_GRID = MAP_grid()


player_render_dist = 300
player_deload_dist = 500
player_speed = 6
player_displacement = VEC()

def get_P_direction(player_displacement_ = None):
    keys = pygame.key.get_pressed()
    direction = VEC()
    direction.x = 0
    direction.y = 0
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
    if not player_displacement_ == None:
        player_displacement_ += direction * player_speed
    return direction * player_speed


