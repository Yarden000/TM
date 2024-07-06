'''
this file is only used for testing and wont be used in the game
'''

import numpy as np
import pygame, sys
import random
import math
import time

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

    def __init__(self)-> None:
        self.ranges_list: list[tuple[float, float]] = []

    def corect_boundries(self, angular_range:tuple[float, float]) -> tuple[float, float]:
        '''checks if boundries are false,
        for example: if the range doues more than
        a full rotation or if the end crossed the zero point'''
        start, end = angular_range

        if start >= end:
            print('possible eror: start of angular range bigger or equal than end', (start, end))
            delta = (start - end) // (2 * self.pi) + 1
            end += delta * 2 * self.pi

        # if start not between 0 and 2*pi it corrects
        redundance = start // (2 * self.pi)
        start -= redundance * 2 * self.pi
        end -= redundance * 2 * self.pi

        # if range more than entire circle
        if end - start >= 2 * self.pi:
            start, end = 0, 2 * self.pi

        return (start, end)
        
    def combined_ranges(self, angular_range_1:tuple[float, float], angular_range_2:tuple[float, float]) -> tuple[float, float] | None:
        start_1, end_1 = self.corect_boundries(angular_range_1)
        start_2, end_2 = self.corect_boundries(angular_range_2)
        
        if start_1 <= start_2:

            if start_2 > end_1:
                # there is a hole
                return None
            return self.corect_boundries((start_1, end_2))
        
        if start_1 > end_2:
            # there is a hole
            return None
        return self.corect_boundries((start_2, end_1))

    def add_to_list(self, new_angular_range:tuple[float, float]) -> None:
        '''adds a range to the ranges_list without redundant overlap'''
        new_ranges_list: list[tuple[float, float]] = []
        for ang_range in self.ranges_list:
            if combined_range := self.combined_ranges(ang_range, new_angular_range):
                new_angular_range = combined_range
            else:
                new_ranges_list.append(ang_range)
        new_ranges_list.append(new_angular_range)
        self.ranges_list = new_ranges_list

    def sub(self, new_angular_range:tuple[float, float]) -> None:
        '''removes a range to the ranges_list without redundant overlap'''
        pass

    def invert(self) -> None:
        '''
        inverts the ranges_list:
        what was in the ranges is now out and what was out is now in
        '''
        pass


angular_range_handeler = AngularRangeHandeler()
ranes_list = [(4, 5), (0, math.pi), (3, 4.5)]
for r in ranes_list:
    angular_range_handeler.add_to_list(r)

print(angular_range_handeler.ranges_list)