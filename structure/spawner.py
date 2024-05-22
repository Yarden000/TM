import random as rnd
from entities import Entity


class Spawner:
    def __init__(self, camera, map, displayable_entenies):
        self.spawn_range = 1  # number of chunks loaded
        self.camera = camera
        self.map = map
        # FIXME: I guess that the Spawner shouldn't manage the displayable
        # properties
        self.displayable_entenies = displayable_entenies

    def spawn_test_ent(self, pos=(0, 0), size=64, image='../graphics/test/none.png'):
        # test
        test_entity = Entity(pos, size, image)
        self.displayable_entenies.append(test_entity)

    def _spawn_ent(self, entity_class, pos):
        # FIXME: not clear that ent is a class and that a new object is beeing instanciated
        entity = entity_class(pos)
        if not entity.collide_state():
            self.displayable_entenies.append(entity)
        else:
            entity.kill()

    def _tiles_loaded(self):
        # décalage si chunk_number est impaire
        d_x = (self.map.chunk_number / 2) % 2 * self.map.chunk_size_in_pixel
        d_y = d_x

        tmpx = self.map.chunk_number / 2 + (d_x - self.camera.true_player_displacement[0]) // self.map.chunk_size_in_pixel
        # FIXME: same idea for tmpy and tile...
        chunk_range_x = (int(tmpx - self.spawn_range), int(tmpx + self.spawn_range))
        chunk_range_y = (int(self.map.chunk_number / 2 + (d_y - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel - self.spawn_range), int(self.map.chunk_number / 2 + (d_y - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel + self.spawn_range))

        tile_x = chunk_range_x[0] * self.map.chunk_size
        tile_range_x = range(tile_x, tile_x + 1)  # +1 because last one doesnt count in a range
        tile_y = chunk_range_y[0] * self.map.chunk_size
        tile_range_y = range(tile_y, tile_y + 1)
        # print(tile_range_x)
        # print(tile_range_y)

        tiles_ordered = [
            {'type': i['type'], 'tiles': []}
            for i in self.map.biome_types
        ]

        # FIXME: parait trop compliqué
        for i in tile_range_x:
            for j in tile_range_y:
                if 0 <= i < self.map.map_size and 0 <= j < self.map.map_size:
                    for n, biome in enumerate(self.map.biome_types):
                        if self.map.grid[i][j][0]['type'] == biome['type']:
                            tiles_ordered[n]['tiles'].append(self.map.grid[i][j])
                            break

        # FIXME: why not?:
        tile_x_start = (
            int(
                self.map.chunk_number / 2
                + (d_x - self.camera.true_player_displacement[0]) // self.map.chunk_size_in_pixel
                - self.spawn_range
            ) * self.map.chunk_size
        )
        tile_x_start = max(0, tile_x_start)
        tile_x_end = (
            int(
                self.map.chunk_number / 2
                + (d_x - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel
                - self.spawn_range
            ) * self.map.chunk_size
        )
        tile_x_end = min(grid_size, tile_x_min)
        tile_y_start = (
            int(
                self.map.chunk_number / 2
                + (d_y - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel
                - self.spawn_range
            ) * self.map.chunk_size
        )
        tile_y_end = (
            int(
                self.map.chunk_number / 2
                + (d_y - self.camera.true_player_displacement[1]) // self.map.chunk_size_in_pixel
                - self.spawn_range
            ) * self.map.chunk_size
        )
        for row in self.map.grid[tile_x_start:tile_x_end]:
            for tile in row[tile_y_start:tile_y_end]:
                # tile is now self.map.grid[i][j]
                for n, biome in enumerate(self.map.biome_types):
                    if tile[0]['type'] == biome['type']:
                        tiles_ordered[n]['tiles'].append(tile)
                        break

        return tiles_ordered

    def density(self, pos):
        region = tuple(pos // Entity.region_size)
        dist = 2
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[0] + j)
                if region_ in Entity.regions:
                    n += len(Entity.regions[region_])
        density = n / ((dist * Entity.region_size) * (dist * Entity.region_size)) * 100000   # the *100000 is because the density is very small
        print(density)
        return density

    def spawn_ent(self, dt, ent):
        limit = 3
        for i in self._tiles_loaded():
            prob = ent.spawning_rates[i['type']] * dt
            for j in i['tiles']:
                density = self.density(j[1])
                if 0 < density < limit:
                    if rnd.randint(0, 1000) < prob * 200 / (density * 2):
                        self._spawn_ent(ent, j[1])
                        self.entity_manager.add_new_entity(entity_class, j[i])



class RessourceSpawner(Spawner):
    def __init__(self):
        super().__init__()


class AnimalSpawner(Spawner):
    def __init__(self):
        super().__init__()


class StructureSpawner(Spawner):
    def __init__(self):
        super().__init__()
