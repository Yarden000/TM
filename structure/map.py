'''map calculations'''
from random import (
    random,
    randrange,
    randint
    )
import math
import pygame
import numpy
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
        self.chunk_number = 3  # number of chunks
        self.chunk_size = 5  # number of tiles in a chunk
        self.chunk_size_in_pixel = self.chunk_size * self.cell_size
        self.map_size = self.chunk_number * self.chunk_size
        self.biome_types = [
            {'type': 'desert', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/desert.png').convert(), (self.cell_size, self.cell_size))},
            {'type': 'plains', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/plains.png').convert(), (self.cell_size, self.cell_size))},
            {'type': 'forest', 'image': pygame.transform.scale(pygame.image.load('../graphics/test/forest.png').convert(), (self.cell_size, self.cell_size))}
        ]

        map_gen = MapGenerator(self.map_size, self.cell_size, self.biome_types)  # (self.map_size, self.biome_types[, base_gris_size, octaves, persistence, frequency, random])
        self.grid = map_gen.make_map()

    def _range_on_screen(self, camera) -> tuple[range, range]:
        '''Calculate horizontal range (x-axis) visible on screen'''
        # the + 0.1 is for when the map_size if odd it rounds it to the number above
        start_x = round(((self.map_size + 0.1) / 2) - ((WIDTH + camera.player_displacement[0]) // self.cell_size))
        end_x = round(((self.map_size + 0.1) / 2) + ((WIDTH - camera.player_displacement[0]) // self.cell_size)) + 1
        range_x = range(start_x, end_x)

        '''Calculate vertical range (y-axis) visible on screen'''
        # the + 0.1 is for when the map_size if odd it rounds it to the number above
        start_y = round(((self.map_size + 0.1) / 2) - ((HEIGHT + camera.player_displacement[1]) // self.cell_size))
        end_y = round(((self.map_size + 0.1) / 2) + ((HEIGHT - camera.player_displacement[1]) // self.cell_size)) + 1
        range_y = range(start_y, end_y)

        return (range_x, range_y)

    def display(self, camera) -> None:
        '''displays only the tiles that are on the screen'''
        range_on_screen = self._range_on_screen(camera)
        for x in range_on_screen[0]:
            if 0 <= x < self.map_size:
                for y in range_on_screen[1]:
                    if 0 <= y < self.map_size:
                        image = self.grid[x][y][0]['image']
                        image_rect = image.get_rect(center=VEC_2(self.grid[x][y][1] + camera.player_displacement))
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
    def __init__(self, map_size, cell_size, biome_types, base_grid_size=3, octaves=6, persistence=0.5, frequency=2, random_prob=0.00015) -> None:
        self.cell_size = cell_size
        self.biome_types = biome_types
        self.biome_number = len(self.biome_types)
        self.cell_number = map_size
        self.base_grid_size = base_grid_size
        self.octaves = octaves
        self.persistence = persistence
        self.frequency = frequency
        self.random_prob = random_prob

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

    def _create_random_uni_vec(self) -> tuple[float, float]:
        angle = random()*360
        return math.cos(angle), math.sin(angle)

    def _create_vector_grid(self, grid_size) -> numpy.ndarray[tuple[float, float]]:
        '''
        creates a grid of random vectors
        '''
        return numpy.array(
            [
                [
                    self._create_random_uni_vec()
                    for _ in range(grid_size + 1)
                ]
                for _ in range(grid_size + 1)
            ]
        )

    def _perlin_dot(self, v1: tuple[float, float], v2: tuple[float, float]) -> float:
        return v1[0] * v2[0] + v1[1] * v2[1]

    def _perlin_noise_at_point(self, i, j, grid_size, vector_grid, octave) -> float:
        '''
        calculates the perlin noise value at a single point
        '''
        # finding the position in the perlin_grid
        x = ((i + 0.5) * grid_size) / self.cell_number
        y = ((j + 0.5) * grid_size) / self.cell_number
        # finding in whitch cell of the perlin grid the point is
        i, j = int(x), int(y)
        # finding the relative position in the cell
        cell_x, cell_y = x % 1, y % 1
        # dot products
        dot_topleft = self._perlin_dot(
            vector_grid[i][j + 1],
            (cell_x, cell_y - 1)
        )
        dot_topright = self._perlin_dot(
            vector_grid[i + 1][j + 1],
            (cell_x - 1, cell_y - 1)
        )
        dot_bottomleft = self._perlin_dot(
            vector_grid[i][j],
            (cell_x, cell_y)
        )
        dot_bottomright = self._perlin_dot(
            vector_grid[i + 1][j],
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

    def _simple_perlin_noise(self, grid_size: int, octave: int) -> list[list[float]]:
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

    def _complex_perlin_noise(self) -> list[list[float]]:
        total_value_grid = []
        grid_size = self.base_grid_size
        for p in range(self.octaves):
            value_grid = self._simple_perlin_noise(grid_size, p)
            if p == 0:
                total_value_grid = [
                    [y for y in x]
                    for x in value_grid
                ]

            else:
                for i in range(self.cell_number):
                    for j in range(self.cell_number):
                        total_value_grid[i][j] += value_grid[i][j]

            grid_size *= self.frequency

        return total_value_grid

    def _get_max_biome_val(self, x, y, grid) -> tuple[dict[str, str | pygame.surface.Surface], tuple[float, float]]:
        value = 0
        idx = 0
        for i, biome in enumerate(grid):
            tmp = biome[x][y]
            if tmp > value:
                idx = i
                value = tmp
        pos = (VEC_2(x, y) - VEC_2(self.cell_number - 1,  self.cell_number - 1) / 2) * self.cell_size
        return (self.biome_types[idx], pos)

    def _simple_superposition(self) -> list[list[tuple[dict[str, str | pygame.surface.Surface], tuple[float, float]]]]:
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

    def make_map(self):
        '''makes map'''
        return self._simple_superposition()
