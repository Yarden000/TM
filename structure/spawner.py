import pygame, sys
import random as rnd
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )
from entities import (
    Entity
)

class Spawner:
    
    def __init__(self, camera, map, displayable_entenies):
        self.spawn_range = 1 #number of chunks loaded
        self.camera = camera
        self.map = map
        self.displayable_entenies = displayable_entenies

    def _spawn_ent(self, ent, pos):
        entity = ent(pos)
        if entity.collide_state() == False:
            self.displayable_entenies.append(entity)
            #print(entity.region)
        else:
            entity.kill()
            print('kill')

    def _tiles_loaded(self):
        # décalage si chunk_number est impaire
        d_x = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel
        d_y = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel

        chunk_range_x = (int(self.map.chunk_number / 2 + (d_x - self.camera.true_player_displacement[0]) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (d_x - self.camera.true_player_displacement[0]) // self.map.chunk_size_in_pixel + self.spawn_range))
        chunk_range_y = (int(self.map.chunk_number / 2 + (d_y - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (d_y - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel + self.spawn_range))
        tile_range_x = range(chunk_range_x[0] * self.map.chunk_size, chunk_range_x[1] * self.map.chunk_size + 1) # +1 because last one doesnt count in a range
        tile_range_y = range(chunk_range_y[0] * self.map.chunk_size, chunk_range_y[1] * self.map.chunk_size + 1)
        #print(tile_range_x)
        #print(tile_range_y)
        
        tiles_ordered = [ 
            {'type': i['type'], 'tiles': []} for i in self.map.biome_types
        ]

        for i in tile_range_x:
            for j in tile_range_y:
                if 0 <= i < self.map.map_size and 0 <= j < self.map.map_size:
                    for n, biome in enumerate(self.map.biome_types):
                        if self.map.grid[i][j][0]['type'] == biome['type']:
                            tiles_ordered[n]['tiles'].append(self.map.grid[i][j])
                            break
                        
        return tiles_ordered
    
    def density(self, pos):
        region = tuple(pos // Entity.region_size)
        dist = 1
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[0] + j)
                if region_ in Entity.regions:
                    n += len(Entity.regions[region_])
        density = n / ((dist * Entity.region_size) * (dist * Entity.region_size)) * 100000   # the *100000 is because the density is very small
        return density

    def spawn_ent(self, dt, ent):
        limit = 100
        density_scaling = 1
        for i in self._tiles_loaded():
            prob = ent.spawning_rates[i['type']] * dt
            for j in i['tiles']:
                pos = j[1] + VEC_2(rnd.randint((-(self.map.cell_size - ent.size) / 2), (self.map.cell_size - ent.size) / 2), 
                                   rnd.randint((-(self.map.cell_size - ent.size) / 2), (self.map.cell_size - ent.size) / 2))
                density = self.density(pos)
                if 0 < density < limit:
                    if rnd.randint(0, 1000) < prob * 1000 / (density * density_scaling):
                        self._spawn_ent(ent, pos)


            
class RessourceSpawner(Spawner):

    def __init__(self):
        super().__init__()



class AnimalSpawner(Spawner):

    def __init__(self):
        super().__init__()



class StructureSpawner(Spawner):

    def __init__(self):
        super().__init__()
