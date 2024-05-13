import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )
from entities import (
    Entity
)

class Spawner:
    
    def __init__(self, camera, map, chunks, displayable_entenies):
        self.spawn_range = 1 #number of chunks loaded
        self.camera = camera
        self.map = map
        self.chunks = chunks
        self.displayable_entenies = displayable_entenies

    def spawn_test_ent(self, pos = (0, 0), size = 64, image = '../graphics/test/none.png'):
        # test
        test_entity = Entity(pos, size, image)
        self.displayable_entenies.append(test_entity)

    def tiles_loaded(self):
        # décalage si chunk_number est impaire
        d_x = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel
        d_y = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel

        chunk_range_x = (int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[0] + d_x) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[0] + d_x) // self.map.chunk_size_in_pixel + self.spawn_range))
        chunk_range_y = (int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[1] + d_y) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[1] + d_y) // self.map.chunk_size_in_pixel + self.spawn_range))
        tile_range_x = range(chunk_range_x[0] * self.map.chunk_size, chunk_range_x[1] * self.map.chunk_size)
        tile_range_y = range(chunk_range_y[0] * self.map.chunk_size, chunk_range_y[1] * self.map.chunk_size)
        #print(tile_range_x)
        #print(tile_range_y)
        all_desert_tiles = []
        all_plains_tiles = []
        all_forest_tiles = []
        for i in tile_range_x:
            for j in tile_range_y:
                if  0 < i < self.map.map_size and 0 < j < self.map.map_size:
                    if self.map.grid[i][j][0]['name'] == 'desert':
                        all_desert_tiles.append(self.map.grid[i][j])
                    elif self.map.grid[i][j][0]['name'] == 'plains':
                        all_plains_tiles.append(self.map.grid[i][j])
                    else:
                        all_forest_tiles.append(self.map.grid[i][j])
        print(len(all_desert_tiles), len(all_plains_tiles), len(all_forest_tiles))   # faux pour l'instant
        
class RessourceSpawner(Spawner):

    def __init__(self):
        super().__init__()



class AnimalSpawner(Spawner):

    def __init__(self):
        super().__init__()



class StructureSpawner(Spawner):

    def __init__(self):
        super().__init__()
