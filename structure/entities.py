import pygame, sys
import random
import math
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )


class EntityManager:
    def __init__(self):
        self.regions = {}
        self.region_size = 1000  # needs to be bigger than all entity sizes
        self.entity_list = []

    def add_player(self, player):
        self.player = player
        self.add_new_entity(self.player)
        
    def _spawn_ent(self, ent_class, pos, overide = False): 
        ent = ent_class(pos)
        self.add_new_entity(ent)
        if (not self.entity_colision_state(ent) == False) and not overide:
            self.remove_entity(ent)

    def add_new_entity(self, entity):
        self.entity_list.append(entity)
        region = tuple(entity.pos // self.region_size)
        entity.region = region
        if region in self.regions:
            self.regions[region].append(entity)
            #print('add')
        else:
            self.regions[region] = [entity]
            #print('new')

    def entity_colision_state(self, ent):
        ents_collided_with = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[0] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        dist = ent.pos.distance_to(ent_.pos)
                        if dist < (ent.size + ent_.size) / 2 and ent_ != ent:
                            ents_collided_with.append(ent_)
        if len(ents_collided_with) == 0:
            return False
        return ents_collided_with
    
    def ent_density(self, pos):
        #region = tuple(self.entity_manager.player.pos // self.entity_manager.region_size) # test
        region = tuple(pos // self.region_size)
        dist = 2
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[0] + j)
                if region_ in self.regions:
                    n += len(self.regions[region_])
        density = n / (((dist + 1) * self.region_size) * ((dist + 1) * self.region_size)) * 10000   # the *100000 is because the density is very small
        return density

    def remove_entity(self, ent):
        self.regions[ent.region].remove(ent)
        self.entity_list.remove(ent)
        del ent

    def run(self, dt, camera):
        self.player.run(dt, camera)

        for ent in self.entity_list:
            if not ent == self.player:
                ent.run(dt)
            else:  # debugging
                #print(tuple(self.player.pos // self.region_size))
                pass

    def draw_regions(self, player_displacement):
        r = 20
        for i in range(-r, r + 1):
            k = i * self.region_size
            pygame.draw.line(pygame.display.get_surface(), 'red', VEC_2(-r* self.region_size, k) + player_displacement, VEC_2(r* self.region_size, k) + player_displacement)
            pygame.draw.line(pygame.display.get_surface(), 'red', VEC_2(k, -r* self.region_size) + player_displacement, VEC_2(k, r* self.region_size) + player_displacement)



class Entity:
    # class for all the enteties: ressouces, animals...
    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 0}
    movable = False
    size = 64

    def __init__(self, pos):
        self.pos = VEC_2(pos)

        self.region = 'meh'
        
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/none.png'), (__class__.size, __class__.size))

    def display(self, screen, camera):
        if -self.size / 2 < self.pos.x + camera.player_displacement.x < WIDTH + self.size / 2:
            if -self.size / 2 < self.pos.y + camera.player_displacement.y < HEIGHT + self.size / 2:
                screen.blit(self.image, self.image.get_rect(center = VEC_2(self.pos + camera.player_displacement)))

    def run(self, dt):
        pass


class Ressource(Entity):
    # for debugging:
    spawning_rates = {'desert': 1, 'plains': 1, 'forest': 1}
    #spawning_rates = {'desert': 0, 'plains': 0.2, 'forest': 0}

    def __init__(self, camera):
        super().__init__(camera)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/ressource.png'), (__class__.size, __class__.size))



class Animal(Entity):
     # for debugging:
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 0}
    #spawning_rates = {'desert': 0, 'plains': 0, 'forest': 1}
    movable = True

    def __init__(self, camera):
        super().__init__(camera)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/animal.png'), (self.size, self.size))
        # for testing
        self.direction = VEC_2(math.sin(random.randint(0, 360) / math.pi), math.cos(random.randint(0, 360) / math.pi))
        

    def move(self, dt):
        self.pos += self.direction * dt * 20


    def run(self, dt):
        self.move(dt)
        



class Structure(Entity):

    def __init__(self):
        super().__init__()


