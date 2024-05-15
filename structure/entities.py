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

    def __init__(self, pos):
        self.pos = VEC_2(pos)

        self.region = tuple(self.pos // __class__.region_size)
        if self.region in __class__.regions:
            __class__.regions[self.region].append(self)
        else:
            __class__.regions[self.region] = [self]

        self.size = 64
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/none.png'), (self.size, self.size))

      
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
        return ents_collided_with
    
    def kill(self):
        __class__.regions[self.region].remove(self)
        del self

    def run(self, dt):
        pass


class Ressource(Entity):
    spawning_rates = {'desert': 0, 'plains': 0.2, 'forest': 0}

    def __init__(self, camera):
        super().__init__(camera)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/ressource.png'), (self.size, self.size))



class Animal(Entity):
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 1}

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


