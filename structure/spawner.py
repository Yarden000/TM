'''the passive random spawning of entities'''
import random as rnd
import pygame
from settings import (
    VEC_2
    )


class Spawner:
    '''respomnsible for spawning the entities'''
    def __init__(self, camera, map, entity_manager) -> None:
        self.spawn_range = 3000  # needs to be smaller than map.map_gen.load_dist
        self.camera = camera
        self.map = map
        self.entity_manager = entity_manager
        # testing
        self.remainder = 0

    def _tiles_loaded(self):

        tiles_ordered = [
            {'type': i['type'], 'tiles': []} for i in self.map.biome_types
        ]

        tiles_range_x = range(int((self.camera.true_player_displacement[0] - self.spawn_range) // self.map.cell_size),
                              int((self.camera.true_player_displacement[0] + self.spawn_range) // self.map.cell_size))
        
        tiles_range_y = range(int((self.camera.true_player_displacement[1] - self.spawn_range) // self.map.cell_size),
                              int((self.camera.true_player_displacement[1] + self.spawn_range) // self.map.cell_size))

        for i in tiles_range_x:
            for j in tiles_range_y:
                if (i, j) in self.map.grid:
                    tile = self.map.grid[(i, j)]
                    for n, biome in enumerate(self.map.biome_types):
                        if tile[0]['type'] == biome['type']:
                            tiles_ordered[n]['tiles'].append(tile)
                            break
        return tiles_ordered

    def spawn_ent_v2(self, dt, ent_class) -> None:
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
                possible_room_for_noise = self.map.cell_size / 2
                pos = tile[1] + VEC_2(rnd.randint(-int(possible_room_for_noise), int(possible_room_for_noise)),
                                      rnd.randint(-int(possible_room_for_noise), int(possible_room_for_noise)))
                self.entity_manager.spawn_ent(ent_class(pos, self.entity_manager))  # time problem in here
