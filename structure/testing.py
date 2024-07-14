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


class AngularRangeHandeler:
    '''used for the Sight
    all angles must be in rads'''
    pi = math.pi

    def __init__(self, ranges_list: list[tuple[float, float]] = []) -> None:
        self.ranges_list = ranges_list

    def clear(self) -> None:
        self.ranges_list = []

    def sort(self) -> None:
        def key_function(x):
            return x[0]
        self.ranges_list.sort(key = key_function)

    def are_equal(self, ranges_list_1, ranges_list_2) -> bool:
        ranges_list_1 = self.remove_null_ranges(ranges_list_1)
        ranges_list_2 = self.remove_null_ranges(ranges_list_2)
        for angular_range in ranges_list_2:
            if angular_range not in ranges_list_1:
                return False
        for angular_range in ranges_list_1:
            if angular_range not in ranges_list_2:
                return False
        return True

    def remove_null_ranges(self, ranges_list) -> list[tuple[float, float]]:
        new_ranges_list = []
        for range_ in ranges_list:
            if range_[0] != range_[1]:
                new_ranges_list.append(range_)
        return  new_ranges_list

    def corect_boundries(self, angular_range:tuple[float, float]) -> tuple[float, float]:
        '''checks if boundries are false,
        for example: if the range does more than
        a full rotation or if the end crossed the zero point'''
        start, end = angular_range
        
        if start == 2 * self.pi and end == 0:  # equivilent to null range
            return (0, 0)

        # if range more than entire circle
        if end - start >= 2 * self.pi:
            start, end = 0, 2 * self.pi

        # if start not between 0 and 2*pi it corrects
        redundance = start // (2 * self.pi)
        start -= redundance * 2 * self.pi
        end -= redundance * 2 * self.pi

        return (start, end)
        
    def combined_ranges(self, angular_range_1:tuple[float, float], angular_range_2:tuple[float, float]) -> tuple[float, float] | None:
        start_1, end_1 = self.corect_boundries(angular_range_1)
        start_2, end_2 = self.corect_boundries(angular_range_2)

        
        # check to see if they wrap arrount zero
        cross_1 = True if start_1 > end_1 else False
        cross_2 = True if start_2 > end_2 else False

        if cross_1 and cross_2:
            # they both cross zero so no need to check for a hole

            if start_1 <= start_2:

                if end_2 <= end_1:
                    return self.corect_boundries((start_1, end_1))
                if end_2 < start_1:
                    return self.corect_boundries((start_1, end_2))
                return (0, 2 * self.pi)
                
            # start_1 > start_2
            if end_1 <= end_2:
                return self.corect_boundries((start_2, end_2))
            if end_1 < start_2:
                return self.corect_boundries((start_2, end_1))
            return (0, 2 * self.pi)

        elif cross_1:
            if end_1 >= start_2:
                if end_2 >= start_1:
                    return (0, 2 * self.pi)
                if end_1 >= end_2:
                    return self.corect_boundries((start_1, end_1))
                return self.corect_boundries((start_1, end_2))
            if end_2 >= start_1:
                if start_1 <= start_2:
                    return self.corect_boundries((start_1, end_1))
                return self.corect_boundries((start_2, end_1))
            # hole
            return None
        
        elif cross_2:
            if end_2 >= start_1:
                if end_1 >= start_2:
                    return (0, 2 * self.pi)
                if end_2 >= end_1:
                    return self.corect_boundries((start_2, end_2))
                return self.corect_boundries((start_2, end_1))
            if end_1 >= start_2:
                if start_2 <= start_1:
                    return self.corect_boundries((start_2, end_2))
                return self.corect_boundries((start_1, end_2))
            # hole
            return None
        else:
            if start_1 <= start_2:
                if start_2 > end_1:
                    # there is a hole
                    return None
                if end_2 >= end_1:
                    return self.corect_boundries((start_1, end_2))
                else:
                    return self.corect_boundries((start_1, end_1))
            if start_1 > end_2:
                # there is a hole
                return None
            if end_1 >= end_2:
                return self.corect_boundries((start_2, end_1))
            else:
                return self.corect_boundries((start_2, end_2))

    def add(self, new_angular_range:tuple[float, float]) -> None:
        '''adds a range to the ranges_list without redundant overlap'''
        new_ranges_list: list[tuple[float, float]] = []
        for ang_range in self.ranges_list:
            if combined_range := self.combined_ranges(ang_range, new_angular_range):
                new_angular_range = self.corect_boundries(combined_range)
            else:
                new_ranges_list.append(self.corect_boundries(ang_range))
        new_ranges_list.append(self.corect_boundries(new_angular_range))
        self.ranges_list = new_ranges_list

    def sub(self, new_angular_range:tuple[float, float]) -> None:
        '''removes a range to the ranges_list without redundant overlap'''
        self.invert()        
        self.add(new_angular_range)
        self.invert()

    def invert(self) -> None:
        '''
        inverts the ranges_list:
        what was in the ranges is now out and what was out is now in
        '''
        temp = self.remove_null_ranges(self.ranges_list)
        self.ranges_list = temp
        self.sort()
        new_ranges_list: list[tuple[float, float]] = []
        nbr_of_ranges = len(self.ranges_list)
        if nbr_of_ranges != 0:
            for i in range(nbr_of_ranges):
                this_one = i
                nextone = i + 1 if i < nbr_of_ranges - 1 else 0
                new_range = (self.ranges_list[this_one][1], self.ranges_list[nextone][0])
                new_ranges_list.append(self.corect_boundries(new_range))
        else:
            new_ranges_list = [(0, 2 * self.pi)]
        self.ranges_list = self.remove_null_ranges(new_ranges_list)

    def fits(self, angular_range:tuple[float, float]) -> bool:
        '''checkes if a range could fit in the ranges_list without overlap'''
        original_list = self.ranges_list
        self.sub(angular_range)
        if self.are_equal(original_list, self.ranges_list):
            return True
        self.ranges_list = original_list
        return False
        
    def covers(self, angular_range:tuple[float, float]) -> bool:
        '''checkes if a range would be compleatly covered by the ranges in the list'''
        state = False
        self.invert()
        if self.fits(angular_range):
            state = True
        self.invert()
        return state



'''angular_range_handeler = AngularRangeHandeler()
r = (2.4, 3.99999)
angular_range_handeler.add(r)
angular_range_handeler.invert()
angular_range_handeler.add(r)'''

class Game:
    '''game class'''
    def __init__(self) -> None:
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        flags =  pygame.DOUBLEBUF| pygame.HWSURFACE  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((800, 800), flags, 16)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.set_alpha(None)

        # test
        WIDTH_, HEIGHT_ = pygame.display.get_window_size()
        # print(WIDTH_, HEIGHT_)

        pygame.display.set_caption('Survivorio')

        self.q_key = False
        self.w_key = False
        self.e_key = False


        self.clock = pygame.time.Clock()
        # self.compiler_for_testing_map_gen = CompilerForTestingMapGen()   # enable this and dissable compiler to test map gen

        self.screen = pygame.display.get_surface()
        self.angular_range_handeler = AngularRangeHandeler()


    def draw_ranges(self):
        for angular_range in self.angular_range_handeler.ranges_list:
            rect = pygame.rect.Rect((200, 200), (400, 400))
            pygame.draw.arc(self.screen, 'green', rect, angular_range[0], angular_range[1], width = 10)

    

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
                
            # print(angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400)))
            other_key_pressed = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_c] and not other_key_pressed:
                other_key_pressed = True
                self.angular_range_handeler.clear()
                print(self.angular_range_handeler.ranges_list)

            if keys[pygame.K_q] and not other_key_pressed:
                other_key_pressed = True
                if self.q_key == False:
                    self.q_key = True
                    angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                    self.range_start = angle
            elif not other_key_pressed:
                if self.q_key == True:
                    self.q_key = False
                    angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                    self.range_end = angle
                    self.angular_range_handeler.add((self.range_start, self.range_end))
                    print(self.angular_range_handeler.ranges_list)

            if keys[pygame.K_w] and not other_key_pressed:
                other_key_pressed = True
                if self.w_key == False:
                    self.w_key = True
                    angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                    self.range_start = angle
            elif not other_key_pressed:
                if self.w_key == True:
                    self.w_key = False
                    angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                    self.range_end = angle
                    self.angular_range_handeler.sub((self.range_start, self.range_end))
                    print(self.angular_range_handeler.ranges_list)

            if keys[pygame.K_e] and not other_key_pressed:
                other_key_pressed = True
                if self.e_key == False:
                    self.e_key = True
                    angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                    self.range_start = angle
            elif not other_key_pressed:
                if self.e_key == True:
                    self.e_key = False
                    angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                    self.range_end = angle
                    stare = self.angular_range_handeler.covers((self.range_start, self.range_end))
                    print(stare)


            self.screen.fill('black')
            if self.q_key:
                pygame.draw.line(self.screen, 'blue', VEC_2(400, 400), VEC_2(math.cos(-self.range_start), math.sin(-self.range_start)) * 200 + VEC_2(400, 400), 5)
                pygame.draw.line(self.screen, 'blue', VEC_2(400, 400), VEC_2(pygame.mouse.get_pos()), 5)
                rect = pygame.rect.Rect((250, 250), (300, 300))
                angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                pygame.draw.arc(self.screen, 'blue', rect, self.range_start, angle, width = 10)

            if self.w_key:
                pygame.draw.line(self.screen, 'red', VEC_2(400, 400), VEC_2(math.cos(-self.range_start), math.sin(-self.range_start)) * 200 + VEC_2(400, 400), 5)
                pygame.draw.line(self.screen, 'red', VEC_2(400, 400), VEC_2(pygame.mouse.get_pos()), 5)
                rect = pygame.rect.Rect((250, 250), (300, 300))
                angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                pygame.draw.arc(self.screen, 'red', rect, self.range_start, angle, width = 10)

            if self.e_key:
                pygame.draw.line(self.screen, 'purple', VEC_2(400, 400), VEC_2(math.cos(-self.range_start), math.sin(-self.range_start)) * 200 + VEC_2(400, 400), 5)
                pygame.draw.line(self.screen, 'purple', VEC_2(400, 400), VEC_2(pygame.mouse.get_pos()), 5)
                rect = pygame.rect.Rect((250, 250), (300, 300))
                angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(pygame.mouse.get_pos()) - VEC_2(400, 400))
                pygame.draw.arc(self.screen, 'purple', rect, self.range_start, angle, width = 10)
            
            self.draw_ranges()
            

            pygame.display.update()

            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.clock.tick(60)  # should be FPS
            # print(self.clock.get_fps())
            


if __name__ == '__main__':  # checks if it is the main file
    game = Game()
    game.run()

'''
l = [2.4, 3.99999]
angular_range_handeler.add_to_list(l)
angular_range_handeler.invert()
angular_range_handeler.sub(l)
angular_range_handeler.remove_null_ranges()
'''
