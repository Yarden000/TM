'''map calculations'''
from random import (
    random,
    randrange,
    randint
    )
import math
import pygame
import numpy
from copy import copy
from settings import (
    WIDTH,
    HEIGHT,
    VEC_2,
)


class Map:
    '''responsible for giving the displayer the right tiles and positions for displaying'''
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.cell_size = 200
        self.biome_types = [
            {'type': 'desert', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/desert.png').convert(), (self.cell_size, self.cell_size))},
            {'type': 'plains', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/plains.png').convert(), (self.cell_size, self.cell_size))},
            {'type': 'forest', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/forest.png').convert(), (self.cell_size, self.cell_size))}
        ]

        self.map_gen = MapGenerator(self)  # (self.map_size, self.biome_types[, base_gris_size, octaves, persistence, frequency, random])
        self.grid = {}

    def update(self, pos):
        self.map_gen.update_map_grid(pos)

    def _range_on_screen(self, camera) -> tuple[range, range]:
        range_x = range(int((-camera.true_player_displacement[0] - WIDTH / 2) // self.cell_size),
                        int((-camera.true_player_displacement[0] + WIDTH / 2) // self.cell_size) + 1)
        
        range_y = range(int((-camera.true_player_displacement[1] - HEIGHT / 2) // self.cell_size),
                        int((-camera.true_player_displacement[1] + HEIGHT / 2) // self.cell_size) + 1)

        return (range_x, range_y)

    def display(self, camera) -> None:
        '''displays only the tiles that are on the screen'''
        range_on_screen = self._range_on_screen(camera)
        for x in range_on_screen[0]:
                for y in range_on_screen[1]:
                        if (x, y) in self.grid:
                            image = self.grid[(x, y)][0]['image']
                            image_rect = image.get_rect(center=VEC_2(self.grid[(x, y)][1] + camera.player_displacement))
                            self.screen.blit(image, image_rect)


class MapGeneratorTesting:
    '''visualises the mag gen, helps to finetune the parameters'''
    def __init__(self, biome_number, pixel_sise, base_grid_size=4, octaves=1, persistence=0.5, frequency=2, random_prob=0) -> None:
        self.biome_number = biome_number
        self.pixel_size = pixel_sise
        self.base_gris_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.cell_number = int(max(HEIGHT, WIDTH) / self.pixel_size)
        self.random_prob = random_prob

        self.extreme = 0

    def smooth_step_1(self, x: float) -> float:
        '''smoothing funcion whith first and second derivative equal to 0 if 0 < x < 1'''
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return (6 * x**5) - (15 * x**4) + (10 * x**3)

    def smooth_step_2(self, x: float) -> float:
        '''smoothing funcion whith first derivative equal to 0 if 0 < x < 1'''
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return (3 * x**2) - (2 * x**3)

    def smooth_step_3(self, x: float) -> float:
        '''smoothing funcion '''
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return x

    def perlin_noise(self):
        '''creates the random noise'''
        total_value_grid = {}
        total_value_list = []  # for finding the max and min to then map then on a scale of 0-255
        for p in range(self.octaves):
            grid_size = round(self.base_gris_size * (self.frequency**p))
            perlin_grid = {}
            for x in range(grid_size + 1):
                for y in range(grid_size + 1):
                    angle = randrange(0, 360)
                    perlin_grid[(x, y)] = VEC_2(math.cos(angle), math.sin(angle))

            # creates a grid of values
            value_grid = {}
            for x in range(self.cell_number):
                for y in range(self.cell_number):
                    # finding the position in the perlin_grid
                    _x = ((x + 0.5) * (grid_size)) / self.cell_number
                    _y = ((y + 0.5) * (grid_size)) / self.cell_number
                    # finding the relative position in the cell
                    cell_pos = (_x % 1, _y % 1)
                    # gradient vectors of the vertecies
                    vortex_vector_bottomleft = perlin_grid[(int(_x), int(_y))]
                    vortex_vector_bottomright = perlin_grid[(int(_x) + 1, int(_y))]
                    vortex_vector_topleft = perlin_grid[(int(_x), int(_y) + 1)]
                    vortex_vector_topright = perlin_grid[(int(_x) + 1, int(_y) + 1)]
                    # displacement vectors from the point to the vertecies
                    vect_to_vort_bottomleft = VEC_2(_x % 1, _y % 1)  # .normalize()
                    vect_to_vort_bottomright = VEC_2((_x % 1) - 1, _y % 1)  # .normalize()
                    vect_to_vort_topleft = VEC_2(_x % 1, (_y % 1) - 1)  # .normalize()
                    vect_to_vort_topright = VEC_2((_x % 1) - 1, (_y % 1) - 1)  # .normalize()
                    # dot products
                    dot_topleft = vortex_vector_topleft.dot(vect_to_vort_topleft)
                    dot_topright = vortex_vector_topright.dot(vect_to_vort_topright)
                    dot_bottomleft = vortex_vector_bottomleft.dot(vect_to_vort_bottomleft)
                    dot_bottomright = vortex_vector_bottomright.dot(vect_to_vort_bottomright)
                    # interpolation
                    top_inter = dot_topleft + self.smooth_step_1(cell_pos[0]) * (dot_topright - dot_topleft)
                    bottom_inter = dot_bottomleft + self.smooth_step_1(cell_pos[0]) * (dot_bottomright - dot_bottomleft)
                    value = (bottom_inter + self.smooth_step_1(cell_pos[1]) * (top_inter - bottom_inter)) * (self.persistence**p)
                    value_grid[(x, y)] = value + randint(round(-100 * self.random_prob), round(100 * self.random_prob)) / 2000

            for x in range(self.cell_number):
                for y in range(self.cell_number):
                    if (x, y) in total_value_grid:
                        total_value_grid[(x, y)] += value_grid[(x, y)]
                    else:
                        total_value_grid[(x, y)] = value_grid[(x, y)]

        # used for the display_strengths
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                total_value_list.append(total_value_grid[(x, y)])
        _max, _min = max(total_value_list), min(total_value_list)
        self.extreme = max([_max, abs(_min)])

        return total_value_grid

    def simple_superposition(self):
        '''chooses whitch biome is in witch cell based on their value strength'''
        all_biome_grid = {}
        final_biome_grid = {}
        for i in range(self.biome_number):
            all_biome_grid[i] = self.perlin_noise()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                values = []
                biome_type = []
                for j in range(self.biome_number):
                    values.append(all_biome_grid[j][(x, y)])
                    biome_type.append(j)
                final_biome_grid[(x, y)] = biome_type[values.index(max(values))]
        return final_biome_grid

    def display_biomes(self):  # for testing
        '''displays withch biomes are at what pixel'''
        colors_list = []
        for _ in range(self.biome_number):
            colors_list.append((randint(0, 255), randint(0, 255), randint(0, 255)))
        grid = self.simple_superposition()
        display_surf = pygame.display.get_surface()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                pygame.draw.rect(display_surf, colors_list[grid[(x, y)]], [x*self.pixel_size, y*self.pixel_size, self.pixel_size, self.pixel_size])

    def display_strengths(self):  # for testing
        '''siaplays the strength of the perlin noise at each pixel'''
        grid = self.perlin_noise()
        display_surf = pygame.display.get_surface()
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                if grid[(x, y)] > 0.01:   # 0:#
                    color = (0, round((grid[(x, y)] * 255) / self.extreme), 0)
                elif grid[(x, y)] < -0.01:
                    color = (round(abs(grid[(x, y)] * 255) / self.extreme), 0, 0)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(display_surf, color, [x*self.pixel_size, y*self.pixel_size, self.pixel_size, self.pixel_size])


class MapGenerator:
    '''generates the map grid'''
    def __init__(self, map, base_grid_size=3, octaves=4, persistence=0.6, frequency=2, random_noise_strength=0.05) -> None:
        self.map = map
        self.cell_size = copy(map.cell_size)
        self.biome_types = copy(map.biome_types)
        self.biome_number = len(self.biome_types)

        self.base_grid_size = base_grid_size

        self.octaves = octaves  # nbr of octaves 
        self.persistence = persistence  # next octaves strength 
        self.frequency = frequency  # frequency of next octave
        self.random_noise_strength = random_noise_strength

        # all gradients for all biomes = [ all gradient octaves for a biome = [ grid of gradient vectors= [] ] ]
        self.gradients = [[{} for i in range(self.octaves)] for j in range(self.biome_number)]  

        self.load_dist = 5000
        self.initial_gradient_vec_dist = self.cell_size * 50  # distance between each gradient vector in the first octave, kind of arbitrairy

    def update_map_grid(self, player_pos):
        tiles_range_x = range(int((player_pos[0] - self.load_dist) // self.cell_size), int((player_pos[0] + self.load_dist) // self.cell_size))
        tiles_range_y = range(int((player_pos[1] - self.load_dist) // self.cell_size), int((player_pos[1] + self.load_dist) // self.cell_size))
        for i in tiles_range_x:
            for j in tiles_range_y:
                if (i, j) not in self.map.grid:
                    pos = ((i + 0.5) * self.cell_size, (j + 0.5) * self.cell_size) # position of the cell
                    biome = self.biome_at_point(pos)
                    self.map.grid[(i, j)] = (biome, pos)
    
    def biome_at_point(self, pos):
        strongest = -float('inf')
        winning_biome = None
        for biome in range(self.biome_number):
            strentgh = self.complex_perlin_noise_at_point(pos, biome)
            if strentgh > strongest:
                strongest = strentgh
                winning_biome = biome
        return self.biome_types[winning_biome]

    def complex_perlin_noise_at_point(self, pos, biome):
        total = 0
        for octave in range(self.octaves):
            gradient_vects_coord, relative_pos = self.surrounding_grad_vects_coord(pos, octave)

            self.update_gradients(gradient_vects_coord, octave, biome)
            
            gradients = [self.gradients[biome][octave][coordinate] for coordinate in gradient_vects_coord]
            strength = self._perlin_noise_at_point(relative_pos, octave, gradients)
            total += strength

        return total

    def update_gradients(self, gradient_vects_coord, octave, biome):
        '''if gradient vector not yet created, it is created'''
        for coordinate in gradient_vects_coord:
            if coordinate not in self.gradients[biome][octave]:
                # random gradient_vect
                self.gradients[biome][octave][coordinate] = VEC_2(0, 1).rotate(random() * 360)

    def surrounding_grad_vects_coord(self, pos, octave):
        '''findes the relative coordinates of the gradient vectors around a point
        and the relative position of said point in the box of vectors'''

        dist = self.initial_gradient_vec_dist / self.frequency ** octave  # distance between two gradient vectors (the size of the box)

        # coordinates of the gradient vectors surrounding the point (the unites are the distance between the gradients)
        x_small = pos[0] // dist
        x_big = x_small + 1
        y_small = pos[1] // dist
        y_big = y_small + 1

        gradient_vects_coor = [(x_small, y_big), (x_big, y_big),
                          (x_small, y_small), (x_big, y_small)]
        
        # are equivalent
        '''
        relative_pos = ((pos[0] - x_small * dist) / dist,
                        (pos[1] - y_small * dist) / dist)
                        '''
        relative_pos = (pos[0] / dist - x_small,
                        pos[1] / dist - y_small)
        return gradient_vects_coor, relative_pos

    def _smooth_step_1(self, x: float) -> float:
        if x < 0:
            raise ValueError
        elif x > 1:
            raise ValueError
        else:
            return (6*x*x - 15*x + 10)*x*x*x

    def _smooth_step_2(self, x: float) -> float:
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return (3 * x**2) - (2 * x**3)

    def _smooth_step_3(self, x: float) -> float:
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return x

    def _perlin_dot(self, v1: tuple[float, float], v2: tuple[float, float]) -> float:
        return v1[0] * v2[0] + v1[1] * v2[1]

    def _perlin_noise_at_point(self, relative_pos, octave, gradients) -> float:
        '''
        calculates the perlin noise value at a single point
        '''
        cell_x, cell_y = relative_pos
        # dot products
        dot_topleft = self._perlin_dot(
            gradients[0],
            (cell_x, cell_y - 1)
        )
        dot_topright = self._perlin_dot(
            gradients[1],
            (cell_x - 1, cell_y - 1)
        )
        dot_bottomleft = self._perlin_dot(
            gradients[2],
            (cell_x, cell_y)
        )
        dot_bottomright = self._perlin_dot(
            gradients[3],
            (cell_x - 1, cell_y)
        )
        # interpolation
        smooth_x = self._smooth_step_1(cell_x)
        smooth_y = self._smooth_step_1(cell_y)
        top_inter = dot_topleft + smooth_x * (dot_topright - dot_topleft)
        bottom_inter = dot_bottomleft + smooth_x * (dot_bottomright - dot_bottomleft)
        return (
            (bottom_inter + smooth_y * (top_inter - bottom_inter)) * (self.persistence**octave)
            + (random() - 0.5) * self.random_noise_strength
        )


class F:
    def __init__(self):
        self.load_dist = 5000
        self.tile_size = 500
        self.nbr_of_biomes = 4
        self.initial_gradient_vec_dist = self.tile_size * 50  # kind of arbitrairy
        self.octaves = 4  # nbr of octaves 
        self.persistence = 0.5  # next octaves strength 
        self.frequency = 2  # frequency of next octave
        self.tile_grid = {}
        self.gradient_vec_grids = [{} for i in self.octaves]

    def f(self, player_pos):
        tiles_range_x = ((player_pos[0] - self.load_dist) // self.tile_size, (player_pos[0] + self.load_dist) // self.tile_size)
        tiles_range_y = ((player_pos[1] - self.load_dist) // self.tile_size, (player_pos[1] + self.load_dist) // self.tile_size)
        for i in range(tiles_range_x):
            for j in range(tiles_range_y):
                if (i, j) not in self.grid:
                    pos = ((i + 0.5) * self.tile_size, (j + 0.5) * self.tile_size)
                    biome = self.biome_at_point(pos)
                    self.tile_grid[(i, j)] = (biome, pos)

    def biome_at_point(self, pos):
        for octave in range(self.octaves):
            gradient_vects_pos = self.surrounding_grad_vects(pos, octave)
            for coordinate in gradient_vects_pos:

                if coordinate not in self.gradient_vec_grids[octave]:
                    # random gradient_vect
                    self.gradient_vec_grids[octave] = VEC_2(0, 1).rotate(randrange(0, 360))

                

    def surrounding_grad_vects(self, pos, octave):
        dist = self.initial_gradient_vec_dist / self.frequency ** octave
        # coordinates of the gradient vectors surrounding the point (the unites are the distance between the gradients)
        x_small = pos[0] // dist
        x_big = x_small + 1
        y_small = pos[1] // dist
        y_big = y_small + 1
        gradient_vects_pos = [(x_small, y_big), (x_big, y_big),
                          (x_small, y_small), (x_big, y_small)]
        return gradient_vects_pos


  
    
