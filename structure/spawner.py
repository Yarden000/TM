'''the passive random spawning of entities'''
import random as rnd
from settings import (
    VEC_2
    )


class Spawner:
    '''respomnsible for spawning the entities'''
    def __init__(self, camera, terrain, entity_manager):
        self.spawn_range = 3  # number of chunks loaded
        self.camera = camera
        self.terrain = terrain
        self.entity_manager = entity_manager
        # testing
        self.remainder = 0

    def _tiles_loaded(self):

        tiles_ordered = [
            {'type': i['type'], 'tiles': []} for i in self.terrain.biome_types
        ]

        # décalage si chunk_number est impaire
        d = (self.terrain.chunk_number / 2) % 2 * self.terrain.chunk_size_in_pixel
        # print(d)

        chunk_in_x = self.terrain.chunk_number / 2 + (d - self.camera.true_player_displacement[0]) // self.terrain.chunk_size_in_pixel
        chunk_in_y = self.terrain.chunk_number / 2 + (d - self.camera.true_player_displacement[1]) // self.terrain.chunk_size_in_pixel

        chunk_range_x = (int(chunk_in_x - self.spawn_range), int(chunk_in_x + self.spawn_range))
        chunk_range_y = (int(chunk_in_y - self.spawn_range), int(chunk_in_y + self.spawn_range))

        tile_range_x = (chunk_range_x[0] * self.terrain.chunk_size, chunk_range_x[1] * self.terrain.chunk_size)
        tile_range_y = (chunk_range_y[0] * self.terrain.chunk_size, chunk_range_y[1] * self.terrain.chunk_size)

        tile_x_start = min(self.terrain.map_size, max(0, tile_range_x[0]))
        tile_x_end = min(self.terrain.map_size, max(0, tile_range_x[1]))
        tile_y_start = min(self.terrain.map_size, max(0, tile_range_y[0]))
        tile_y_end = min(self.terrain.map_size, max(0, tile_range_y[1]))
        # print((tile_x_start, tile_x_end), (tile_y_start, tile_y_end))
        for row in self.terrain.grid[tile_x_start:tile_x_end + 1]:
            for tile in row[tile_y_start:tile_y_end + 1]:
                for n, biome in enumerate(self.terrain.biome_types):
                    if tile[0]['type'] == biome['type']:
                        tiles_ordered[n]['tiles'].append(tile)
                        break
        return tiles_ordered

    def spawn_ent_v2(self, dt, ent_class):
        '''randomly chooses a tile fron all the loaded tiles and spawns an enitiy there'''
        tiles_loaded = self._tiles_loaded()  # not the speed problem
        density = self.entity_manager.ent_density()
        for i in tiles_loaded:
            # calculates the number of ents to spawn for a biome type
            number = ent_class.spawning_rates[i['type']] * dt * len(i['tiles']) / (density * density + 1)
            remainder = number - int(number)
            if self.remainder >= 1 - remainder:
                number = int(number + 1)
                self.remainder -= 1 - remainder
            else:
                self.remainder += remainder
                number = 0
            # spawns the entities
            tiles = rnd.choices(i['tiles'], k=number)
            for tile in tiles:
                possible_room_for_noise = self.terrain.cell_size / 2 - ent_class.radius
                pos = tile[1] + VEC_2(rnd.randint(-possible_room_for_noise, possible_room_for_noise),
                                      rnd.randint(-possible_room_for_noise, possible_room_for_noise))
                self.entity_manager.spawn_ent(ent_class(pos, self.entity_manager))  # time problem in here
