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

    def _tiles_loaded(self):
        # décalage si chunk_number est impaire
        d_x = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel
        d_y = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel

        chunk_range_x = (int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[0] + d_x) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[0] + d_x) // self.map.chunk_size_in_pixel + self.spawn_range))
        chunk_range_y = (int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[1] + d_y) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (WIDTH / 2 - self.camera.player_displacement[1] + d_y) // self.map.chunk_size_in_pixel + self.spawn_range))
        tile_range_x = range(chunk_range_x[0] * self.map.chunk_size, chunk_range_x[1] * self.map.chunk_size + 1) # +1 because last one doesnt count in a range
        tile_range_y = range(chunk_range_y[0] * self.map.chunk_size, chunk_range_y[1] * self.map.chunk_size + 1)
        #print(tile_range_x)
        #print(tile_range_y)
        
        tiles_ordered = [ 
            {'type': i['type'], 'tiles': []} for i in self.map.biome_types
        ]

        for i in tile_range_x:
            for j in tile_range_y:
                for n, biome in enumerate(self.map.biome_types):
                    if self.map.grid[i][j][0]['type'] == biome['type']:
                        tiles_ordered[n]['tiles'].append(self.map.grid[i][j])
                        break
                        
        return tiles_ordered
    
    def spawn_ent(self, ent):
        prob = 0
        for i in self._tiles_loaded():
            prob += len(i['tiles']) * ent.spawning_rates[i['type']]
        print(prob)
            


        

        
class RessourceSpawner(Spawner):

    def __init__(self):
        super().__init__()



class AnimalSpawner(Spawner):

    def __init__(self):
        super().__init__()



class StructureSpawner(Spawner):

    def __init__(self):
        super().__init__()