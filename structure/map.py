import pygame, sys, random, math
import numpy as np
import settings
from settings import map_size, WIDTH, HEIGHT, cell_size, VEC_2, biome_types



class Map:

    def __init__(self, camera):
        self.screen = pygame.display.get_surface()
        self.grid = settings.map_grid
        self.camera = camera

    def range_on_screen(self):
        self.range_x = range(round((map_size / 2) - ((WIDTH + self.camera.player_displacement[0]) // cell_size)), round((map_size / 2) + ((WIDTH - self.camera.player_displacement[0]) // cell_size)) + 1)    # +1 is buffer
        self.range_y = range(round((map_size / 2) - ((HEIGHT + self.camera.player_displacement[1]) // cell_size)), round((map_size / 2) + ((HEIGHT - self.camera.player_displacement[1]) // cell_size)) + 1)
        return (self.range_x, self.range_y)
        
    def display(self):
        self.range = self.range_on_screen()
        for x in self.range[0]:
            if 0 < x < map_size:
                for y in self.range[1]:
                    if 0 < y < map_size:
                        self.pos = (VEC_2(x, y) - VEC_2(map_size -1,  map_size -1) / 2) * cell_size + self.camera.player_displacement
                        self.image = self.grid[x][y]['image']
                        self.screen.blit(self.image, self.pos)


class MapGenerator_testing:
    
    def __init__(self, biome_number, pixel_sise, base_grid_size = 4, octaves = 1, persistence = 0.5, frequency = 2, random_prob = 0):
        self.biome_number = biome_number
        self.pixel_size = pixel_sise
        self.base_gris_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.cell_number = int(max(settings.HEIGHT, settings.WIDTH) / self.pixel_size)
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
    
    def __init__(self, base_grid_size = 4, octaves = 1, persistence = 0.5, frequency = 2, random_prob = 0):
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

    def create_random_uni_vec(self):
        self.angle = random.randrange(0, 360)
        return VEC_2(math.cos(self.angle), math.sin(self.angle))

    def create_vector_grid(self, grid_size):
        '''
        creates a grid of random vectors
        '''
        self.vector_grid = [
            [self.create_random_uni_vec() for y in range(grid_size + 1)] for x in range(grid_size + 1)
            ]
        return self.vector_grid

    def perlin_noise_at_point(self,x, y, cell_number, grid_size, vector_grid, octave):
        '''
        calculates the perlin noise value at a single point
        '''
        # finding the position in the perlin_grid
        self.x = ((x + 0.5) * (grid_size)) / cell_number
        self.y = ((y + 0.5) * (grid_size)) / cell_number
        # finding in whitch cell of the perlin grid the point is
        self.perlin_grid_cell = (int(self.x), int(self.y))
        # finding the relative position in the cell
        self.cell_pos = (self.x % 1, self.y % 1)
        # gradient vectors of the vertecies
        self.vortex_vector_bottomleft = vector_grid[int(self.x)][int(self.y)]
        self.vortex_vector_bottomright = vector_grid[int(self.x) + 1][int(self.y)]
        self.vortex_vector_topleft = vector_grid[int(self.x)][int(self.y) + 1]
        self.vortex_vector_topright = vector_grid[int(self.x) + 1][int(self.y) + 1]
        # displacement vectors from the point to the vertecies
        self.vect_to_vort_bottomleft = VEC_2(self.x % 1, self.y % 1)#.normalize()
        self.vect_to_vort_bottomright = VEC_2((self.x % 1) - 1, self.y % 1)#.normalize()
        self.vect_to_vort_topleft = VEC_2(self.x % 1, (self.y % 1) - 1)#.normalize()
        self.vect_to_vort_topright = VEC_2((self.x % 1) - 1, (self.y % 1) - 1)#.normalize()
        # dot products
        self.dot_topleft = self.vortex_vector_topleft.dot(self.vect_to_vort_topleft)
        self.dot_topright = self.vortex_vector_topright.dot(self.vect_to_vort_topright)
        self.dot_bottomleft = self.vortex_vector_bottomleft.dot(self.vect_to_vort_bottomleft)
        self.dot_bottomright = self.vortex_vector_bottomright.dot(self.vect_to_vort_bottomright)
        # interpolation
        self.top_inter = self.dot_topleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_topright - self.dot_topleft)
        self.bottom_inter = self.dot_bottomleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_bottomright - self.dot_bottomleft)
        self.value = (self.bottom_inter + self.smooth_step_1(self.cell_pos[1]) * (self.top_inter - self.bottom_inter)) * (self.persistence**octave)
        self.value += random.randint(-100, 100) * self.random_prob / 2000
        return self.value

    def simple_perlin_noise(self, cell_number, grid_size, vector_grid, octave):
        '''
        creates a grid of simple(only one octave) perlin-noise values
        '''
        self.perlin_grid = [
            [
                self.perlin_noise_at_point(x, y, cell_number, grid_size, vector_grid, octave) for y in range(cell_number)
            ]for x in range(cell_number)
        ]                
        return self.perlin_grid
    
    def complex_perlin_noise(self):
        self.total_value_grid = []
        for p in range(self.octaves):
            self.grid_size = round(self.base_grid_size * (self.frequency**p))
            self.vector_grid = self.create_vector_grid(self.grid_size)
            self.value_grid = self.simple_perlin_noise(self.cell_number, self.grid_size, self.vector_grid, p)
            

            self.row = 0
            if p == 0:
                self.total_value_grid = [
                    [
                        y for y in x
                    ] for x in self.value_grid
                ]

            else:
                for x in range(self.cell_number):
                    self.col = 0
                    for y in range(self.cell_number):
                        self.total_value_grid[x][y] += self.value_grid[x][y]
                        self.col += 1
                    self.row += 1
          
        return(self.total_value_grid)
    
    def get_max_biome_val(self, x, y):
        self.values = [self.all_biome_grid[i][x][y] for i in range(self.biome_number)]
        return self.biome_types[self.values.index(max(self.values))]

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
        self.all_biome_grid = [self.complex_perlin_noise() for i in range(self.biome_number)]
        self.final_biome_grid = [
            [
                self.get_max_biome_val(x, y) for y in range(self.cell_number)
            ] for x in range(self.cell_number) 
        ]
        #'''

        return(self.final_biome_grid)
    
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