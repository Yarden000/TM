import pygame, sys
import random as rnd
from settings import (
    debug, 
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )
from entities import (
    Entity
)

class Spawner:
    
    def __init__(self, camera, map, entity_manager):
        self.spawn_range = 10 #number of chunks loaded
        self.camera = camera
        self.map = map
        self.entity_manager = entity_manager
        # testing
        self.remainder = 0
      
    def _tiles_loaded(self):

        tiles_ordered = [ 
            {'type': i['type'], 'tiles': []} for i in self.map.biome_types
        ]

        # décalage si chunk_number est impaire
        d = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel
        #print(d)

        chunk_in_x = self.map.chunk_number / 2 + (d - self.camera.true_player_displacement[0]) // self.map.chunk_size_in_pixel
        chunk_in_y = self.map.chunk_number / 2 + (d - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel

        chunk_range_x = (int(chunk_in_x - self.spawn_range), int(chunk_in_x + self.spawn_range))
        chunk_range_y = (int(chunk_in_y - self.spawn_range), int(chunk_in_y + self.spawn_range))

        tile_range_x = (chunk_range_x[0] * self.map.chunk_size, chunk_range_x[1] * self.map.chunk_size)
        tile_range_y = (chunk_range_y[0] * self.map.chunk_size, chunk_range_y[1] * self.map.chunk_size)
        
        tile_x_start = min(self.map.map_size, max(0, tile_range_x[0]))
        tile_x_end = min(self.map.map_size, max(0, tile_range_x[1]))
        tile_y_start = min(self.map.map_size, max(0, tile_range_y[0]))
        tile_y_end = min(self.map.map_size, max(0, tile_range_y[1]))
        #print((tile_x_start, tile_x_end), (tile_y_start, tile_y_end))
        for row in self.map.grid[tile_x_start:tile_x_end + 1]:
            for tile in row[tile_y_start:tile_y_end + 1]:
                for n, biome in enumerate(self.map.biome_types):
                    if tile[0]['type'] == biome['type']:
                        tiles_ordered[n]['tiles'].append(tile)
                        break          
        return tiles_ordered
    
    def density(self, pos):
        region = tuple(self.entity_manager.player.pos // self.entity_manager.region_size) # test
        #region = tuple(pos // self.entity_manager.region_size)
        dist = 1
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.entity_manager.regions:
                    n += len(self.entity_manager.regions[region_])
        density = n / (((dist + 1) * self.entity_manager.region_size) * ((dist + 1) * self.entity_manager.region_size)) * 10000   # the *100000 is because the density is very small
        return density

    def spawn_ent(self, dt, ent_class):
        limit = 100
        density_scaling = 1
        for i in self._tiles_loaded():
            prob = ent_class.spawning_rates[i['type']] * dt
            for j in i['tiles']:
                pos = j[1] + VEC_2(rnd.randint((-(self.map.cell_size - ent_class.size) / 2), (self.map.cell_size - ent_class.size) / 2), 
                                   rnd.randint((-(self.map.cell_size - ent_class.size) / 2), (self.map.cell_size - ent_class.size) / 2))
                density = self.entity_manager.ent_density(pos)
                if 0 < density < limit:
                    if rnd.randint(0, 1000) < prob * 1000 / (density * density_scaling):
                        self._spawn_ent(ent_class, pos)

    def spawn_ent_v2(self, dt, ent_class):
        for i in self._tiles_loaded():
            '''calculates the number of ents to spawn for a biome type'''  # needs to include density
            number = ent_class.spawning_rates[i['type']] * dt * len(i['tiles'])
            remainder = number - int(number)
            if self.remainder >= 1 - remainder:
                number = int(number + 1)
                self.remainder -= 1 - remainder
            else:
                self.remainder += remainder
                number = 0

            '''spawns the entities'''
            tiles = rnd.choices(i['tiles'], k=number)
            for tile in tiles:
                pos = tile[1] + VEC_2(rnd.randint((-(self.map.cell_size - ent_class.size) / 2), (self.map.cell_size - ent_class.size) / 2), 
                                    rnd.randint((-(self.map.cell_size - ent_class.size) / 2), (self.map.cell_size - ent_class.size) / 2))
                self.entity_manager._spawn_ent(ent_class, pos)

            
class RessourceSpawner(Spawner):

    def __init__(self):
        super().__init__()



class AnimalSpawner(Spawner):

    def __init__(self):
        super().__init__()



class StructureSpawner(Spawner):

    def __init__(self):
        super().__init__()
