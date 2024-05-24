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
        self.cell_size = 200
        self.chunk_number = 10  # number of chunks
        self.chunk_size = 10  # number of tiles in a chunk
        self.chunk_size_in_pixel = self.chunk_size * self.cell_size
        self.map_size = self.chunk_number * self.chunk_size
        self.biome_types = [
            {'type': 'desert', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/desert.png'), (self.cell_size, self.cell_size))},
            {'type': 'plains', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/plains.png'), (self.cell_size, self.cell_size))},
            {'type': 'forest', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/forest.png'), (self.cell_size, self.cell_size))}
        ]

        map_gen = MapGenerator(self.map_size, self.cell_size, self.biome_types)  # (self.map_size, self.biome_types[, base_gris_size, octaves, persistence, frequency, random])
        self.grid = map_gen.make_map()

    def _range_on_screen(self, camera):
        self.range_x = range(round((self.map_size / 2) - ((WIDTH + camera.player_displacement[0]) // self.cell_size)), round((self.map_size / 2) + ((WIDTH - camera.player_displacement[0]) // self.cell_size)) + 2)    # +2 is buffer
        self.range_y = range(round((self.map_size / 2) - ((HEIGHT + camera.player_displacement[1]) // self.cell_size)), round((self.map_size / 2) + ((HEIGHT - camera.player_displacement[1]) // self.cell_size)) + 2)
        return (self.range_x, self.range_y)

    def display(self, camera):
        self.range = self._range_on_screen(camera)
        for x in self.range[0]:
            if 0 <= x < self.map_size:
                for y in self.range[1]:
                    if 0 <= y < self.map_size:
                        self.image = self.grid[x][y][0]['image']
                        self.screen.blit(self.image.convert_alpha(), self.image.get_rect(center = VEC_2(self.grid[x][y][1] + camera.player_displacement)))


class MapGenerator_testing:
    
    def __init__(self, biome_number, pixel_sise, base_grid_size = 4, octaves = 1, persistence = 0.5, frequency = 2, random_prob = 0):
        self.biome_number = biome_number
        self.pixel_size = pixel_sise
        self.base_gris_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.cell_number = int(max(HEIGHT, WIDTH) / self.pixel_size)
        self.random_prob = random_prob

    def smooth_step_1(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return ((6 * x**5) - (15 * x**4) + (10 * x**3))
        
    def smooth_step_2(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return ((3 * x**2) - (2 * x**3))
        
    def smooth_step_3(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return (x)

    def perlin_noise(self):
        self.total_value_grid = {}
        self.total_value_list = [] # for finding the max and min to then map then on a scale of 0-255
        for p in range(self.octaves):
            self.grid_size = round(self.base_gris_size * (self.frequency**p))
            self.perlin_grid = {}
            for x in range(self.grid_size + 1):
                for y in range(self.grid_size + 1):
                    self.angle = random.randrange(0, 360)
                    self.perlin_grid[(x, y)] = settings.VEC_2(math.cos(self.angle), math.sin(self.angle))

            # creates a grid of values
            self.value_grid = {}
            for x in range(self.cell_number):
                for y in range(self.cell_number):
                    # finding the position in the perlin_grid
                    self.x = ((x + 0.5) * (self.grid_size)) / self.cell_number
                    self.y = ((y + 0.5) * (self.grid_size)) / self.cell_number
                    # finding in whitch cell of the perlin grid the point is
                    self.perlin_grid_cell = (int(self.x), int(self.y))
                    # finding the relative position in the cell
                    self.cell_pos = (self.x % 1, self.y % 1)
                    # gradient vectors of the vertecies
                    self.vortex_vector_bottomleft = self.perlin_grid[(int(self.x), int(self.y))]
                    self.vortex_vector_bottomright = self.perlin_grid[(int(self.x) + 1, int(self.y))]
                    self.vortex_vector_topleft = self.perlin_grid[(int(self.x), int(self.y) + 1)]
                    self.vortex_vector_topright = self.perlin_grid[(int(self.x) + 1, int(self.y) + 1)]
                    # displacement vectors from the point to the vertecies
                    self.vect_to_vort_bottomleft = settings.VEC_2(self.x % 1, self.y % 1)#.normalize()
                    self.vect_to_vort_bottomright = settings.VEC_2((self.x % 1) - 1, self.y % 1)#.normalize()
                    self.vect_to_vort_topleft = settings.VEC_2(self.x % 1, (self.y % 1) - 1)#.normalize()
                    self.vect_to_vort_topright = settings.VEC_2((self.x % 1) - 1, (self.y % 1) - 1)#.normalize()
                    # dot products
                    self.dot_topleft = self.vortex_vector_topleft.dot(self.vect_to_vort_topleft)
                    self.dot_topright = self.vortex_vector_topright.dot(self.vect_to_vort_topright)
                    self.dot_bottomleft = self.vortex_vector_bottomleft.dot(self.vect_to_vort_bottomleft)
                    self.dot_bottomright = self.vortex_vector_bottomright.dot(self.vect_to_vort_bottomright)
                    # interpolation
                    self.top_inter = self.dot_topleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_topright - self.dot_topleft)
                    self.bottom_inter = self.dot_bottomleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_bottomright - self.dot_bottomleft)
                    self.value = (self.bottom_inter + self.smooth_step_1(self.cell_pos[1]) * (self.top_inter - self.bottom_inter)) * (self.persistence**p)
                    self.value_grid[(x, y)] = self.value + random.randint(round(-100 * self.random_prob), round(100 * self.random_prob)) / 2000

            for x in range(self.cell_number):
                for y in range(self.cell_number):
                    if (x, y) in self.total_value_grid:
                        self.total_value_grid[(x, y)] += self.value_grid[(x, y)]
                    else:
                        self.total_value_grid[(x, y)] = self.value_grid[(x, y)]

        # used for the display_strengths
        for x in range(self.cell_number):
                for y in range(self.cell_number):
                    self.total_value_list.append(self.total_value_grid[(x, y)])
        self.max, self.min = max(self.total_value_list), min(self.total_value_list)
        self.mid = (self.max + self.min) / 2
        self.extreme = max([self.max, abs(self.min)])

        return(self.total_value_grid)

    def simple_superposition(self):
        # chooses whitch biome is in witch cell based on their value strength
        self.all_biome_grid = {}
        self.final_biome_grid = {}
        for i in range(self.biome_number):
            self.all_biome_grid[i] = self.perlin_noise()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                self.values = []
                self.biome_type = []
                for j in range(self.biome_number):
                    self.values.append(self.all_biome_grid[j][(x, y)])
                    self.biome_type.append(j)
                self.final_biome_grid[(x, y)] = self.biome_type[self.values.index(max(self.values))]
        return(self.final_biome_grid)

    def display_biomes(self, grid): #for testing
        self.colors_list = []
        for i in range(self.biome_number):
            self.colors_list.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.grid = grid
        self.display_surf = pygame.display.get_surface()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                pygame.draw.rect(self.display_surf, self.colors_list[self.grid[(x, y)]], [x*self.pixel_size, y*self.pixel_size, self.pixel_size, self.pixel_size])

    def display_strengths(self, grid): #for testing
        self.grid = grid
        self.display_surf = pygame.display.get_surface()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                if self.grid[(x, y)] > 0.01:   #0:#
                    self.color = (0, round((self.grid[(x, y)] * 255) / self.extreme), 0)
                elif self.grid[(x, y)] < -0.01:
                    self.color = (round(abs(self.grid[(x, y)] * 255) / self.extreme), 0, 0)
                else:
                    self.color = (255, 255, 255)
                pygame.draw.rect(self.display_surf, self.color, [x*self.pixel_size, y*self.pixel_size, self.pixel_size, self.pixel_size])


class MapGenerator:
    def __init__(self, map_size, cell_size, biome_types, base_grid_size=3, octaves=6, persistence=0.5, frequency=2, random_prob=0.00015):
        self.cell_size = cell_size
        self.biome_types = biome_types
        self.biome_number = len(self.biome_types)
        self.cell_number = map_size
        self.base_grid_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.random_prob = random_prob

    def _smooth_step_1(self, x):
        if x < 0:
            raise ValueError
        elif x > 1:
            raise ValueError
        else:
            return (6*x*x - 15*x + 10)*x*x*x

    def _smooth_step_2(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return (3 * x**2) - (2 * x**3)

    def _smooth_step_3(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return x

    def _create_random_uni_vec(self):
        angle = random()*360
        return math.cos(angle), math.sin(angle)

    def _create_vector_grid(self, grid_size):
        '''
        creates a grid of random vectors
        '''
        return array(
            [
                [
                    self._create_random_uni_vec()
                    for _ in range(grid_size + 1)
                ]
                for _ in range(grid_size + 1)
            ]
        )

    def _perlin_dot(self, xy, XY):
        return xy[0]*XY[0] + xy[1]*XY[1]

    def _perlin_noise_at_point(self, i, j, grid_size, vector_grid, octave) -> float:
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
        smooth_x = self._smooth_step_1(cell_x)
        smooth_y = self._smooth_step_1(cell_y)
        top_inter = dot_topleft + smooth_x * (dot_topright - dot_topleft)
        bottom_inter = dot_bottomleft + smooth_x * (dot_bottomright - dot_bottomleft)
        return (
            (bottom_inter + smooth_y * (top_inter - bottom_inter)) * (self.persistence**octave)
            + (random() - 0.5) * self.random_prob
        )

    def _simple_perlin_noise(self, grid_size, octave):
        '''
        creates a grid of simple(only one octave) perlin-noise values
        '''
        vector_grid = self._create_vector_grid(grid_size)
        return [
            [
                self._perlin_noise_at_point(i, j, grid_size, vector_grid, octave)
                for i in range(self.cell_number)
            ] for j in range(self.cell_number)
        ]

    def _complex_perlin_noise(self):
        total_value_grid = []
        grid_size = self.base_grid_size
        for p in range(self.octaves):
            self.value_grid = self._simple_perlin_noise(grid_size, p)
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

    def _get_max_biome_val(self, x, y, grid):
        value = 0
        idx = 0
        for i, biome in enumerate(grid):
            tmp = biome[x][y]
            if tmp > value:
                idx = i
                value = tmp
        pos = (VEC_2(x, y) - VEC_2(self.cell_number -1,  self.cell_number -1) / 2) * self.cell_size
        return (self.biome_types[idx].copy(), pos)  # need to remove the .copy()

    def _simple_superposition(self):
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
        all_biome_grid = [
            self._complex_perlin_noise()
            for i in range(self.biome_number)
        ]
        final_biome_grid = [
            [
                self._get_max_biome_val(i, j, all_biome_grid)
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
        return self._simple_superposition()
