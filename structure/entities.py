import pygame, sys
import random
import math
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )



class Entity:
    regions = {}
    region_size = 1000
    # class for all the enteties: ressouces, animals...
    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 0}
    movable = False
    size = 64

    def __init__(self, pos):
        self.pos = VEC_2(pos)

        self.region = tuple(self.pos // __class__.region_size)
        if self.region in __class__.regions:
            __class__.regions[self.region].append(self)
        else:
            __class__.regions[self.region] = [self]

        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/none.png'), (__class__.size, __class__.size))

    def update_region(self):
        new_region = tuple(self.pos // __class__.region_size)
        if self.region != new_region:
            if new_region in __class__.regions:
                __class__.regions[new_region].append(self)
            else:
                __class__.regions[new_region] = [self]
            if self.region in __class__.regions:
                if self in __class__.regions[self.region]:
                    __class__.regions[self.region].remove(self)
            self.region = new_region

    def display(self, screen, camera):
        if -self.size / 2 < self.pos.x + camera.player_displacement.x < WIDTH + self.size / 2:
            if -self.size / 2 < self.pos.y + camera.player_displacement.y < HEIGHT + self.size / 2:
                screen.blit(self.image, self.image.get_rect(center = VEC_2(self.pos + camera.player_displacement)))

    def collide_state(self):
        ents_collided_with = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (self.region[0] + i, self.region[0] + j)
                if region in __class__.regions:
                    for ent in Entity.regions[region]:
                        dist = self.pos.distance_to(ent.pos)
                        if dist < (self.size + ent.size) / 2 and ent != self:
                            ents_collided_with.append(ent)
        if len(ents_collided_with) == 0:
            return False
        #print('colide')
        return ents_collided_with
    
    def kill(self):
        __class__.regions[self.region].remove(self)
        del self

    def run(self, dt):
        self.update_region()


class Ressource(Entity):
    spawning_rates = {'desert': 0, 'plains': 0.2, 'forest': 0}

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
        

    def move(self, dt):
        self.pos += self.direction * dt * 20


    def run(self, dt):
        self.move(dt)
        self.update_region()
        



class Structure(Entity):

    def __init__(self):
        super().__init__()


