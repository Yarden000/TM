import pygame
from random import random
from numpy import array
import math
from settings import (
    WIDTH,
    HEIGHT,
    VEC_2,
)


class Map:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.cell_size = 20
        self.map_size = 200
        self.biome_types = [
            {'name': 'desert', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/desert.png'), (self.cell_size, self.cell_size))},
            {'name': 'plains', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/plains.png'), (self.cell_size, self.cell_size))},
            {'name': 'forest', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/forest.png'), (self.cell_size, self.cell_size))}
        ]

        map_gen = MapGenerator(self.map_size, self.biome_types)  # (self.map_size, self.biome_types[, base_gris_size, octaves, persistence, frequency, random])
        self.grid = map_gen.make_map()

    def range_on_screen(self, camera):
        self.range_x = range(round((self.map_size / 2) - ((WIDTH + camera.player_displacement[0]) // self.cell_size)), round((self.map_size / 2) + ((WIDTH - camera.player_displacement[0]) // self.cell_size)) + 1)    # +1 is buffer
        self.range_y = range(round((self.map_size / 2) - ((HEIGHT + camera.player_displacement[1]) // self.cell_size)), round((self.map_size / 2) + ((HEIGHT - camera.player_displacement[1]) // self.cell_size)) + 1)
        return (self.range_x, self.range_y)

    def display(self, camera):
        self.range = self.range_on_screen(camera)
        for x in self.range[0]:
            if 0 < x < self.map_size:
                for y in self.range[1]:
                    if 0 < y < self.map_size:
                        self.pos = (VEC_2(x, y) - VEC_2(self.map_size - 1,  self.map_size - 1) / 2) * self.cell_size + camera.player_displacement
                        self.image = self.grid[x][y]['image']
                        self.screen.blit(self.image.convert_alpha(), self.pos)


class MapGenerator:
    def __init__(self, map_size, biome_types, base_grid_size=3, octaves=6, persistence=0.5, frequency=2, random_prob=0.00015):
        self.biome_types = biome_types
        self.biome_number = len(self.biome_types)
        self.cell_number = map_size
        self.base_grid_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.random_prob = random_prob

    def smooth_step_1(self, x):
        if x < 0:
            raise ValueError
        elif x > 1:
            raise ValueError
        else:
            return (6*x*x - 15*x + 10)*x*x*x

    def smooth_step_2(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return (3 * x**2) - (2 * x**3)

    def smooth_step_3(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return x

    def create_random_uni_vec(self):
        angle = random()*360
        return math.cos(angle), math.sin(angle)

    def create_vector_grid(self, grid_size):
        '''
        creates a grid of random vectors
        '''
        return array(
            [
                [
                    self.create_random_uni_vec()
                    for _ in range(grid_size + 1)
                ]
                for _ in range(grid_size + 1)
            ]
        )

    def _perlin_dot(self, xy, XY):
        return xy[0]*XY[0] + xy[1]*XY[1]

    def perlin_noise_at_point(self, i, j, grid_size, vector_grid, octave) -> float:
        '''
        calculates the perlin noise value at a single point
        '''
        # finding the position in the perlin_grid
        x = ((i + 0.5) * grid_size) / self.cell_number
        y = ((j + 0.5) * grid_size) / self.cell_number
        # finding in whitch cell of the perlin grid the point is
        I, J = int(x), int(y)
        # finding the relative position in the cell
        cell_x, cell_y = x % 1, y % 1
        # dot products
        dot_topleft = self._perlin_dot(
            vector_grid[I][J + 1],
            (cell_x, cell_y - 1)
        )
        dot_topright = self._perlin_dot(
            vector_grid[I + 1][J + 1],
            (cell_x - 1, cell_y - 1)
        )
        dot_bottomleft = self._perlin_dot(
            vector_grid[I][J],
            (cell_x, cell_y)
        )
        dot_bottomright = self._perlin_dot(
            vector_grid[I + 1][J],
            (cell_x - 1, cell_y)
        )
        # interpolation
        smooth_x = self.smooth_step_1(cell_x)
        smooth_y = self.smooth_step_1(cell_y)
        top_inter = dot_topleft + smooth_x * (dot_topright - dot_topleft)
        bottom_inter = dot_bottomleft + smooth_x * (dot_bottomright - dot_bottomleft)
        return (
            (bottom_inter + smooth_y * (top_inter - bottom_inter)) * (self.persistence**octave)
            + (random() - 0.5) * self.random_prob
        )

    def simple_perlin_noise(self, grid_size, octave):
        '''
        creates a grid of simple(only one octave) perlin-noise values
        '''
        vector_grid = self.create_vector_grid(grid_size)
        return [
            [
                self.perlin_noise_at_point(i, j, grid_size, vector_grid, octave)
                for i in range(self.cell_number)
            ] for j in range(self.cell_number)
        ]

    def complex_perlin_noise(self):
        total_value_grid = []
        grid_size = self.base_grid_size
        for p in range(self.octaves):
            self.value_grid = self.simple_perlin_noise(grid_size, p)
            if p == 0:
                total_value_grid = [
                    [y for y in x]
                    for x in self.value_grid
                ]

            else:
                for i in range(self.cell_number):
                    for j in range(self.cell_number):
                        total_value_grid[i][j] += self.value_grid[i][j]

            grid_size *= self.frequency

        return total_value_grid

    def get_max_biome_val(self, x, y):
        value = 0
        idx = 0
        for i, biome in enumerate(self.all_biome_grid):
            tmp = biome[x][y]
            if tmp > value:
                idx = i
                value = tmp
        return self.biome_types[idx]

    def simple_superposition(self):
        # chooses whitch biome is in witch cell based on their value strength
        '''
        self.final_biome_grid = []
        self.all_biome_grid = [self.complex_perlin_noise() for i in range(self.biome_number)]
        for x in range(self.cell_number):
            self.final_biome_grid.append([])
            for y in range(self.cell_number):
                self.values = []
                for j in range(self.biome_number):
                    self.values.append(self.all_biome_grid[j][x][y])
                self.final_biome_grid[x].append(biome_types[self.values.index(max(self.values))])
        '''
        self.all_biome_grid = [
            self.complex_perlin_noise()
            for i in range(self.biome_number)
        ]
        final_biome_grid = [
            [
                self.get_max_biome_val(i, j)
                for j in range(self.cell_number)
            ] for i in range(self.cell_number)
        ]
        # '''

        return final_biome_grid

    '''  not used
    def convert_to_pos(self):
        self.map_grid_with_indecies = self.simple_superposition()
        self.map_grid_with_pos = []
        self.x = 0
        for x in self.map_grid_with_indecies:
            self.y = 0
            self.map_grid_with_pos.append([])
            for y in x:
                self.pos = tuple((VEC_2(self.x, self.y) - VEC_2(map_size -1,  map_size -1) / 2) * cell_size)
                self.map_grid_with_pos[2] = self.map_grid_with_indecies[self.x][self.y]
                self.y += 1
            self.x += 1
        return(self.map_grid_with_pos)
    '''

    def make_map(self):
        return self.simple_superposition()
