import pygame, sys, time
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
        self.region_size = 200  # needs to be bigger than all entity sizes
        self.entity_list = []
        self.movable_entity_list = []
        

    def add_player(self, player):
        self.player = player
        self.entity_list.append(self.player)
        self.movable_entity_list.append(self.player)
        self.update_ent_region(self.player)
        
    def _spawn_ent(self, ent_class, pos, overide = False): 
        ent = ent_class(pos)
        self.entity_list.append(ent)
        if ent_class.movable:
            self.movable_entity_list.append(ent)
        self.update_ent_region(ent)
        if (not self.entity_collision_state(ent) == False) and not overide:
            self.remove_entity(ent)

    def update_ent_region(self, entity):
        region = tuple(entity.pos // self.region_size)
        entity.region = region
        if region in self.regions:
            self.regions[region].append(entity)
        else:
            self.regions[region] = [entity]

    def update_regions(self):
        for ent in self.movable_entity_list:
            self.update_ent_region(ent)

    def ent_density(self):
        region = tuple(self.player.pos // self.region_size)
        dist = 5 # radius of regions checked
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.regions:
                    n += len(self.regions[region_])
        density = n / (((dist + 1) * self.region_size) * ((dist + 1) * self.region_size)) * 100000   # the *100000 is because the density is very small
        return density
    
    def entity_collision_state(self, ent, want_list=False):   # needs optimisation
        ents_collided_with = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        dist = ent.pos.distance_to(ent_.pos)
                        if dist < ent.radius + ent_.radius and ent_ != ent:
                            if want_list:
                                ents_collided_with.append(ent_)
                            else:
                                return True
        if len(ents_collided_with) == 0:
            return False
        return ents_collided_with
    
    def update_pushout(self, ent):
        ents_collided_with = self.entity_collision_state(ent, want_list=True)
        if ents_collided_with != False:
            for ent_ in ents_collided_with:
                dist = ent.pos.distance_to(ent_.pos)
                overlap = -(dist - ent.radius - ent_.radius)
                if ent.movable:
                    if ent_.movable:
                        ent.move(overlap * (ent.pos - ent_.pos).normalize() / 2) 
                        ent_.move(-overlap * (ent.pos - ent_.pos).normalize() / 2) 
                        continue
                    ent.move(overlap * (ent.pos - ent_.pos).normalize()) 
                    continue
                if ent_.movable:
                    ent_.move(-overlap * (ent.pos - ent_.pos).normalize())
                    continue
                raise ValueError('Two imovable enteties are colliding')
    
    def colisions(self):
        for ent in self.entity_list:
            self.update_pushout(ent)

    def remove_entity(self, ent):
        self.regions[ent.region].remove(ent)
        self.entity_list.remove(ent)
        del ent

    def run(self, dt):
        self.player.run(dt)
        for ent in self.entity_list:
            if not ent == self.player:
                ent.run(dt)
            else:  # debugging
                #print(tuple(self.player.pos // self.region_size))
                pass
        self.update_regions()
        self.colisions()

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
    radius = size / 2

    def __init__(self, pos):
        self.pos = VEC_2(pos)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/none.png'), (__class__.size, __class__.size))

    def display(self, screen, camera):
        if -self.radius < self.pos.x + camera.player_displacement.x < WIDTH + self.radius:
            if -self.radius < self.pos.y + camera.player_displacement.y < HEIGHT + self.radius:
                screen.blit(self.image, self.image.get_rect(center = VEC_2(self.pos + camera.player_displacement)))

    def move(self, displacement):
        self.pos += displacement

    def run(self, dt):
        pass


class Ressource(Entity):
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 0}

    def __init__(self, camera):
        super().__init__(camera)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/ressource.png'), (__class__.size, __class__.size))



class Animal(Entity):
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 1}
    movable = True

    def __init__(self, camera):
        super().__init__(camera)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/animal.png'), (self.size, self.size))
        # for testing
        self.direction = VEC_2(math.sin(random.randint(0, 360) / math.pi), math.cos(random.randint(0, 360) / math.pi))
        

    def wander(self, dt):
        self.pos += self.direction * dt * 20


    def run(self, dt):
        self.wander(dt)
        



class Structure(Entity):

    def __init__(self):
        super().__init__()


