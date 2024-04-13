import pygame, sys, random, math
import numpy as np
import settings
#from settings import *



class Map:

    def __init__(self, camera):
        self.screen = pygame.display.get_surface()
        self.grid = settings.map_grid
        self.camera = camera

        #screen.blit(image, DEFAULT_IMAGE_POSITION)

    def display(self):
        for k, v in self.grid.items():  # k = key, v = grid[k]
            self.pos_on_screen_x = k[0] + self.camera.player_displacement[0] - settings.cell_size / 2
            self.pos_on_screen_y = k[1] + self.camera.player_displacement[1] - settings.cell_size / 2
            if (-settings.cell_size) < self.pos_on_screen_x < (settings.WIDTH + settings.cell_size / 2):
                if (-settings.cell_size) < self.pos_on_screen_y < (settings.HEIGHT + settings.cell_size / 2):
                    self.image = v['image']
                    self.screen.blit(self.image, (self.pos_on_screen_x, self.pos_on_screen_y))


class MapGenerator_testing:
    
    def __init__(self, biome_number, pixel_sise, base_grid_size = 4, octaves = 1, persistence = 0.5, frequency = 2):
        self.biome_number = biome_number
        self.pixel_size = pixel_sise
        self.base_gris_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.cell_number = int(max(settings.HEIGHT, settings.WIDTH) / self.pixel_size)

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
                    self.amplitude = random.randrange(-1, 1) / 100
                    self.perlin_grid[(x, y)] = settings.VEC_2(math.cos(self.angle), math.sin(self.angle)) * (10**self.amplitude)

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
                    self.dot_topleft = settings.dot(self.vortex_vector_topleft, self.vect_to_vort_topleft)
                    self.dot_topright = settings.dot(self.vortex_vector_topright, self.vect_to_vort_topright)
                    self.dot_bottomleft = settings.dot(self.vortex_vector_bottomleft, self.vect_to_vort_bottomleft)
                    self.dot_bottomright = settings.dot(self.vortex_vector_bottomright, self.vect_to_vort_bottomright)
                    # interpolation
                    self.top_inter = self.dot_topleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_topright - self.dot_topleft)
                    self.bottom_inter = self.dot_bottomleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_bottomright - self.dot_bottomleft)
                    self.value = (self.bottom_inter + self.smooth_step_1(self.cell_pos[1]) * (self.top_inter - self.bottom_inter)) * (self.persistence**p)
                    self.value_grid[(x, y)] = self.value

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
    
    def __init__(self, biome_types, base_grid_size = 4, octaves = 1, persistence = 0.5, frequency = 2):
        self.biome_types = biome_types
        self.biome_number = len(biome_types)
        self.cell_number = settings.map_size
        self.base_grid_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency

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

    def create_vector_grid(self, grid_size):
        '''
        creates a grid of random vectors
        '''
        self.vector_grid = {}
        for x in range(grid_size + 1):
            for y in range(grid_size + 1):
                self.angle = random.randrange(0, 360)
                self.amplitude = random.randrange(-1, 1) / 100 # can be omitted
                self.vector_grid[(x, y)] = settings.VEC_2(math.cos(self.angle), math.sin(self.angle)) * (10**self.amplitude)
        return self.vector_grid

    def simple_perlin_noise(self, cell_number, grid_size, vector_grid, octave):
        '''
        creates a grid of simple(only one octave) perlin-noise values
        '''
        self.perlin_grid = {}
        for x in range(cell_number):
            for y in range(cell_number):
                # finding the position in the perlin_grid
                self.x = ((x + 0.5) * (grid_size)) / cell_number
                self.y = ((y + 0.5) * (grid_size)) / cell_number
                # finding in whitch cell of the perlin grid the point is
                self.perlin_grid_cell = (int(self.x), int(self.y))
                # finding the relative position in the cell
                self.cell_pos = (self.x % 1, self.y % 1)
                # gradient vectors of the vertecies
                self.vortex_vector_bottomleft = vector_grid[(int(self.x), int(self.y))]
                self.vortex_vector_bottomright = vector_grid[(int(self.x) + 1, int(self.y))]
                self.vortex_vector_topleft = vector_grid[(int(self.x), int(self.y) + 1)]
                self.vortex_vector_topright = vector_grid[(int(self.x) + 1, int(self.y) + 1)]
                # displacement vectors from the point to the vertecies
                self.vect_to_vort_bottomleft = settings.VEC_2(self.x % 1, self.y % 1)#.normalize()
                self.vect_to_vort_bottomright = settings.VEC_2((self.x % 1) - 1, self.y % 1)#.normalize()
                self.vect_to_vort_topleft = settings.VEC_2(self.x % 1, (self.y % 1) - 1)#.normalize()
                self.vect_to_vort_topright = settings.VEC_2((self.x % 1) - 1, (self.y % 1) - 1)#.normalize()
                # dot products
                self.dot_topleft = settings.dot(self.vortex_vector_topleft, self.vect_to_vort_topleft)
                self.dot_topright = settings.dot(self.vortex_vector_topright, self.vect_to_vort_topright)
                self.dot_bottomleft = settings.dot(self.vortex_vector_bottomleft, self.vect_to_vort_bottomleft)
                self.dot_bottomright = settings.dot(self.vortex_vector_bottomright, self.vect_to_vort_bottomright)
                # interpolation
                self.top_inter = self.dot_topleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_topright - self.dot_topleft)
                self.bottom_inter = self.dot_bottomleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_bottomright - self.dot_bottomleft)
                self.value = (self.bottom_inter + self.smooth_step_1(self.cell_pos[1]) * (self.top_inter - self.bottom_inter)) * (self.persistence**octave)
                self.perlin_grid[(x, y)] = self.value
        return self.perlin_grid
    
    def complex_perlin_noise(self):
        self.total_value_grid = {}
        for p in range(self.octaves):
            self.grid_size = round(self.base_grid_size * (self.frequency**p))
            self.vector_grid = self.create_vector_grid(self.grid_size)
            self.value_grid = self.simple_perlin_noise(self.cell_number, self.grid_size, self.vector_grid, p)

            for x in range(self.cell_number):
                for y in range(self.cell_number):
                    if (x, y) in self.total_value_grid:
                        self.total_value_grid[(x, y)] += self.value_grid[(x, y)]
                    else:
                        self.total_value_grid[(x, y)] = self.value_grid[(x, y)]

        return(self.total_value_grid)

    def simple_superposition(self):
        # chooses whitch biome is in witch cell based on their value strength
        self.all_biome_grid = {}
        self.final_biome_grid = {}
        for i in range(self.biome_number):
            self.all_biome_grid[i] = self.complex_perlin_noise()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                self.values = []
                for j in range(self.biome_number):
                    self.values.append(self.all_biome_grid[j][(x, y)])
                self.final_biome_grid[(x, y)] = self.biome_types[self.values.index(max(self.values))]
        return(self.final_biome_grid)
    
    def convert_to_pos(self):
        self.map_grid_with_indecies = self.simple_superposition()
        self.map_grid_with_pos = {}
        for i in self.map_grid_with_indecies:
            self.pos = tuple((settings.VEC_2(i) - settings.VEC_2(settings.map_size -1,  settings.map_size -1) / 2) * settings.cell_size)
            self.map_grid_with_pos[self.pos] = self.map_grid_with_indecies[i]
        return(self.map_grid_with_pos)
    
    def make_map(self):
        return self.convert_to_pos()