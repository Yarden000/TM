'''
this file is only used for testing and wont be used in the game
'''

import numpy as np
import pygame, sys
import random
import math
import time
from settings import angle_between_vectors_0_to_2pi, VEC_2

def draw_grid_with_line(grid_size, grid_width, grid_height, line_cells):
    grid = [['-' for _ in range(grid_width)] for _ in range(grid_height)]

    for cell in line_cells:
        grid_y, grid_x = cell
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            grid[grid_y][grid_x] = '#'

    for row in grid:
        print(''.join(row))


def get_grid_cells_for_line_2(start, direction, length, grid_size, thickness):
    '''https://chatgpt.com/c/974e0607-9653-4e22-a183-97e730457388'''
    x0, y0 = start
    dx, dy = direction
    x1 = x0 + length * dx
    y1 = y0 + length * dy

    # Normalize the direction vector
    line_length = math.sqrt(dx**2 + dy**2)
    unit_dx = dx / line_length
    unit_dy = dy / line_length

    # Calculate the perpendicular vector for thickness
    half_thickness = thickness / 2
    perp_dx = -unit_dy * half_thickness
    perp_dy = unit_dx * half_thickness

    # Define the corners of the thick line's bounding rectangle
    corners = [
        (x0 + perp_dx, y0 + perp_dy),
        (x0 - perp_dx, y0 - perp_dy),
        (x1 + perp_dx, y1 + perp_dy),
        (x1 - perp_dx, y1 - perp_dy)
    ]

    # Find the bounding box of the rectangle
    min_x = min(c[0] for c in corners)
    max_x = max(c[0] for c in corners)
    min_y = min(c[1] for c in corners)
    max_y = max(c[1] for c in corners)

    # Convert bounding box to grid coordinates
    def to_grid_coords(x, y):
        return int(math.floor(x / grid_size)), int(math.floor(y / grid_size))

    grid_min_x, grid_min_y = to_grid_coords(min_x, min_y)
    grid_max_x, grid_max_y = to_grid_coords(max_x, max_y)

    # Initialize list of grid cells
    grid_cells = set()

    # Check each cell in the bounding box for intersection with the thick line
    for gx in range(grid_min_x, grid_max_x + 1):
        for gy in range(grid_min_y, grid_max_y + 1):
            cell_x = gx * grid_size
            cell_y = gy * grid_size
            cell_corners = [
                (cell_x, cell_y),
                (cell_x + grid_size, cell_y),
                (cell_x, cell_y + grid_size),
                (cell_x + grid_size, cell_y + grid_size)
            ]

            # Check if any corner of the cell is within the thickness distance from the line
            for cx, cy in cell_corners:
                dx_c = cx - x0
                dy_c = cy - y0
                distance = abs(dy_c * unit_dx - dx_c * unit_dy)
                if distance <= half_thickness:
                    grid_cells.add((gy, gx))
                    break

    return grid_cells


# Example usage
start = (10, 3)
direction = (10, 10)
length = 10
grid_size = 1
thickness = 2
grid_width = 30
grid_height = 15
start_time = time.time()
'''
for i in range(100):
    grid_cells = get_grid_cells_for_line_2(start, direction, length, grid_size, thickness)
end_time = time.time()

draw_grid_with_line(grid_size, grid_width, grid_height, grid_cells)
print(end_time - start_time)
'''

def find_point(p1:VEC_2, v1:VEC_2, p2:VEC_2, s2:float, max_trailing:float=2.0) -> VEC_2:
    dist_vect = p2 - p1
    d = dist_vect.magnitude()
    s1 = v1.magnitude()
    alpha = angle_between_vectors_0_to_2pi(dist_vect, v1)

    tmp = math.sin(alpha) * s1 / s2

    # there is no trajectory where p2 interceps p1
    if tmp > 1:
        tmp = 1
    elif tmp < -1:
        tmp = -1

    beta = math.asin(tmp)

    delta = math.pi - alpha - beta

    t = math.sin(alpha) * d / (s2 * math.sin(delta)) if abs(delta) > 0.00001 else 10000
    t = abs(t)

    print(t, delta)    
    
    if t > d * max_trailing:
        t = d * max_trailing
    
    p3 = p1 + t * v1

    return p3

class Game:
    '''game class'''
    def __init__(self) -> None:
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        flags =  pygame.DOUBLEBUF| pygame.HWSURFACE  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((800, 700), flags, 16)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.set_alpha(None)

        # test
        WIDTH_, HEIGHT_ = pygame.display.get_window_size()
        # print(WIDTH_, HEIGHT_)

        pygame.display.set_caption('Survivorio')

        self.q_key = False
        self.w_key = False
        self.e_key = False

        self.p1 = VEC_2(200, 550)
        self.v1 = VEC_2(0, -1)
        self.s2 = 1.0


        self.clock = pygame.time.Clock()
        # self.compiler_for_testing_map_gen = CompilerForTestingMapGen()   # enable this and dissable compiler to test map gen

        self.screen = pygame.display.get_surface()   

    def run(self) -> None:
        '''runs the game'''
        game_run = True
        while game_run:
            # testing
            # print(self.collision_detector.Rect_Circle({'pos': (2, 2), 'r': 1}, {'pos': (0, 0), 'vec1': VEC_2(1, 1), 'vec2': VEC_2(-1, 1)}))
            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:  # checks if quit
                    pygame.quit()
                    sys.exit()

            p2 = VEC_2(pygame.mouse.get_pos())
            p3 = find_point(self.p1, self.v1, p2, self.s2)
                
            # print(angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400)))
            other_key_pressed = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                self.s2 *= 1.01
            elif keys[pygame.K_w]:
                self.s2 *= 0.99


            self.screen.fill('black')

            pygame.draw.line(self.screen, 'green', self.p1, p2, 5)
            pygame.draw.line(self.screen, 'green', self.p1, p3, 5)
            pygame.draw.line(self.screen, 'green', p3, p2, 5)


            pygame.display.update()

            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.clock.tick(60)  # should be FPS
            # print(self.clock.get_fps())
            
'''

if __name__ == '__main__':  # checks if it is the main file
    game = Game()
    game.run()'''

'''
l = [2.4, 3.99999]
angular_range_handeler.add_to_list(l)
angular_range_handeler.invert()
angular_range_handeler.sub(l)
angular_range_handeler.remove_null_ranges()
'''
if s:
    print('ok')
