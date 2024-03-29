import pygame, sys, random, math
from settings import *


class Map:

    def __init__(self):
        pass

    def display(self):
        pass

    def run(self):
        pass



class MapGenerator:
    
    def _init__(self):
        self.perlin_noise_simple()
        
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


    def perlin_noise_simple(self):
        self.grid_size = 4
        self.perlin_grid = {}
        for x in range(self.grid_size + 1):
            for y in range(self.grid_size + 1):
                self.angle = random.randrange(0, 360)
                self.amplitude = random.randrange(-1, 1) / 100
                self.perlin_grid[(x, y)] = VEC_2(math.cos(self.angle), math.sin(self.angle)) * (10**self.amplitude)


        # creates a grid of values
        self.cell_number = 80 # has to be a multiple of the grid_size
        self.value_grid = {}
        self.value_list = [] # for finding the max and min to then map then on a scale of 0-255
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                # finding the position in the perlin_grid
                self.x = ((x + 0.5) * (self.grid_size)) / self.cell_number
                self.y = ((y + 0.5) * (self.grid_size)) / self.cell_number
                # finding in whitch cell of the perlin grid the point is
                self.perlin_grid_cell = (int(self.x), int(self.y))
                # finding the relative position in the cell
                self.cell_pos = (self.x % 1, self.y % 1)
                #self.cell_pos = (self.x - int(self.x), self.y - int(self.y))
                #print(self.x, self.y)
                #print(self.cell_pos)
                
                # gradient vectors of the vertecies
                self.vortex_vector_bottomleft = self.perlin_grid[(int(self.x), int(self.y))]
                self.vortex_vector_bottomright = self.perlin_grid[(int(self.x) + 1, int(self.y))]
                self.vortex_vector_topleft = self.perlin_grid[(int(self.x), int(self.y) + 1)]
                self.vortex_vector_topright = self.perlin_grid[(int(self.x) + 1, int(self.y) + 1)]
                
                # displacement vectors from the point to the vertecies
                self.vect_to_vort_bottomleft = VEC_2(self.x % 1, self.y % 1)#.normalize()
                self.vect_to_vort_bottomright = VEC_2((self.x % 1) - 1, self.y % 1)#.normalize()
                self.vect_to_vort_topleft = VEC_2(self.x % 1, (self.y % 1) - 1)#.normalize()
                self.vect_to_vort_topright = VEC_2((self.x % 1) - 1, (self.y % 1) - 1)#.normalize()
                
                # dot products
                self.dot_topleft = dot(self.vortex_vector_topleft, self.vect_to_vort_topleft)
                self.dot_topright = dot(self.vortex_vector_topright, self.vect_to_vort_topright)
                self.dot_bottomleft = dot(self.vortex_vector_bottomleft, self.vect_to_vort_bottomleft)
                self.dot_bottomright = dot(self.vortex_vector_bottomright, self.vect_to_vort_bottomright)
                # interpolation
                self.top_inter = self.dot_topleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_topright - self.dot_topleft)
                self.bottom_inter = self.dot_bottomleft + self.smooth_step_1(self.cell_pos[0]) * (self.dot_bottomright - self.dot_bottomleft)
                self.value = self.bottom_inter + self.smooth_step_1(self.cell_pos[1]) * (self.top_inter - self.bottom_inter)
                #self.value = self.dot_topleft
                self.value_list.append(self.value)

                self.value_grid[(x, y)] = self.value
        #print(self.value_grid)

        self.max, self.min = max(self.value_list), min(self.value_list)
        self.mid = (self.max + self.min) / 2
        self.extreme = max([self.max, abs(self.min)])
        #print(self.max, self.min, self.mid, self.extreme)

    def display(self): #test
        self.display_surf = pygame.display.get_surface()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                if self.value_grid[(x, y)] > 0:#0.05:
                    self.color = (0, round((self.value_grid[(x, y)] * 255) / self.extreme), 0)
                elif self.value_grid[(x, y)] < 0:#-0.05:
                    self.color = (round(abs(self.value_grid[(x, y)] * 255) / self.extreme), 0, 0)
                else:
                    self.color = (255, 255, 255)
                #print(self.color)
                pygame.draw.rect(self.display_surf, self.color, [x*WIDTH/self.cell_number, y*HEIGHT/self.cell_number, WIDTH/self.cell_number, HEIGHT/self.cell_number])
