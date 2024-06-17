import pygame, sys, time
import random
import math
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )
from attack import(
    Attack
    )
from collisions import(
    Collision_detector
)

class EntityManager:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.regions = {}
        self.region_size = 200  # needs to be bigger than all entity sizes
        self.entity_list = []
        self.movable_entity_list = []
        self.collision_detector = Collision_detector()
        self.attack = Attack(self)
        

    def inputs(self, dt):
        self.player.move(self.input_manager.player_movement(dt) * self.player.speed)
        # testing
        click = self.input_manager.attack_click()
        if click != None:
            rect = Rectangle(click, self.collision_detector.angle_between_vectors(VEC_2(1, 0), VEC_2(click) - VEC_2(WIDTH, HEIGHT) / 2), 200, 50)
            #print(rect.pos, rect.vec1, rect.vec2)
            self.attack.rect_attack(rect)        

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
        collision_state = self.entity_collision_state(ent, do_pushout=False)
        if collision_state and not overide:
            self.remove_entity(ent)

    def update_ent_region(self, entity):
        region = tuple(entity.hitbox.pos // self.region_size)
        entity.region = region
        if region in self.regions:
            self.regions[region].append(entity)
        else:
            self.regions[region] = [entity]

    def update_regions(self):
        for ent in self.movable_entity_list:
            self.update_ent_region(ent)

    def ent_density(self):
        region = tuple(self.player.hitbox.pos // self.region_size)
        dist = 5 # radius of regions checked
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.regions:
                    n += len(self.regions[region_])
        density = n / (((dist + 1) * self.region_size) * ((dist + 1) * self.region_size)) * 100000   # the *100000 is because the density is very small
        return density
    
    def entity_collision_state(self, ent, do_pushout=False):   # needs optimisation
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        if ent_ != ent:
                            #print(ent, ent_)
                            collisionn_state, pushout = self.collision_detector.collision(ent.hitbox, ent_.hitbox)
                            if collisionn_state:
                                if do_pushout:
                                    #print(ent, ent_, pushout)
                                    self.pushout(ent, ent_, pushout)
                                return True
        return False
    
    def pushout(self, ent, ent_, dissplacement):
        if ent.movable:
            if ent_.movable:
                ent.move(dissplacement / 2) 
                ent_.move(-dissplacement / 2) 
            ent.move(dissplacement) 
        elif not ent_.movable:
            print(ent.movable, ent_.movable)
            raise ValueError('Two imovable enteties are colliding')
    '''
    def entity_collision_state(self, ent, want_list=False):   # needs optimisation
        ents_collided_with = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        if ent_ != ent:
                            collisionn_state, pushout = self.collision_detector.collision(ent.hitbox, ent_.hitbox)
                            if collisionn_state:
                                if want_list:
                                    ents_collided_with.append(ent_)
                                else:
                                    return True, pushout
        if len(ents_collided_with) == 0:
            return False, None
        return ents_collided_with

    def update_pushout_v2(self, ent):
        if ent.movable:
            ents_collided_with = self.entity_collision_state(ent, want_list=True)
            if ents_collided_with != False:
                for ent_ in ents_collided_with:
                    dist = ent.hitbox.pos.distance_to(ent_.hitbox.pos)
                    overlap = -(dist - ent.radius - ent_.radius)
                    if ent_.movable:
                        ent.move(overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize() / 2) 
                        ent_.move(-overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize() / 2) 
                        continue
                    ent.move(overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize()) 
                    
    def update_pushout(self, ent):
        ents_collided_with = self.entity_collision_state(ent, want_list=True)
        if ents_collided_with != False:
            for ent_ in ents_collided_with:
                dist = ent.hitbox.pos.distance_to(ent_.hitbox.pos)
                overlap = -(dist - ent.hitbox.radius - ent_.hitbox.radius)
                if ent.movable:
                    if ent_.movable:
                        ent.move(overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize() / 2) 
                        ent_.move(-overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize() / 2) 
                        continue
                    ent.move(overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize()) 
                    continue
                if ent_.movable:
                    ent_.move(-overlap * (ent.hitbox.pos - ent_.hitbox.pos).normalize())
                    continue
                raise ValueError('Two imovable enteties are colliding')
    '''
    def colisions(self):
        for ent in self.entity_list:
            self.entity_collision_state(ent, do_pushout=True)   

    def remove_entity(self, ent):
        #print(ent)
        self.regions[ent.region].remove(ent)
        self.entity_list.remove(ent)
        del ent

    def run(self, dt):
        self.inputs(dt)
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


class Hitbox:
    kind = None
    def __init__(self, pos):
        self.pos =  VEC_2(pos)

    def scale(self, scalar):
        pass

    def rotate(self, angle):
        pass

    def translate(self, vector):
        pass

class Rectangle(Hitbox):
    kind = 'rect'
    def __init__(self, pos, angle, length, breadth):
        super().__init__(pos)
        angle = angle * 180 / math.pi
        self.vec1 = VEC_2(math.cos(angle), math.sin(angle)) * length
        self.vec2 = VEC_2(math.sin(angle), -math.cos(angle)) * breadth
        

    def scale(self, scalar):
        self.vectors[0] = self.vectors[0] * scalar
        self.vectors[1] = self.vectors[1] * scalar

    def rotate(self, angle):
        self.vectors[0] = self.vectors[0].rotate(angle)
        self.vectors[1] = self.vectors[1].rotate(angle)
    
    def draw(self, display_surface, camera, color):
        #print(self.pos)
        pygame.draw.line(display_surface, color, camera.player_displacement + self.pos + self.vec1 + self.vec2, camera.player_displacement + self.pos + self.vec1 - self.vec2, width = 5)
        pygame.draw.line(display_surface, color, camera.player_displacement + self.pos - self.vec1 + self.vec2, camera.player_displacement + self.pos - self.vec1 - self.vec2, width = 5)
        pygame.draw.line(display_surface, color, camera.player_displacement + self.pos + self.vec2 + self.vec1, camera.player_displacement + self.pos + self.vec2 - self.vec1, width = 5)
        pygame.draw.line(display_surface, color, camera.player_displacement + self.pos - self.vec2 + self.vec1, camera.player_displacement + self.pos - self.vec2 - self.vec1, width = 5)

class Circle(Hitbox):
    kind = 'circle'

    def __init__(self, center, radius):
        super().__init__(center)
        self.r = radius

    def scale(self, scalar):
        self.r = self.r * scalar

    def draw(self, display_surface, camera, color):
        pygame.draw.circle(display_surface, color, camera.player_displacement + self.pos, self.r, 5)


class Entity:
    # class for all the enteties: ressouces, animals...
    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 0}
    movable = False
    size = 64
    radius = size / 2

    def __init__(self, pos):
        self.hitbox = Rectangle(pos, 0, __class__.radius, __class__.radius)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/none.png'), (__class__.size, __class__.size))

    def display(self, screen, camera):
        if -self.radius < self.hitbox.pos.x + camera.player_displacement.x < WIDTH + self.radius:
            if -self.radius < self.hitbox.pos.y + camera.player_displacement.y < HEIGHT + self.radius:
                screen.blit(self.image, self.image.get_rect(center = VEC_2(self.hitbox.pos + camera.player_displacement)))

    def move(self, displacement):
        self.hitbox.pos += displacement

    def run(self, dt):
        pass


class Ressource(Entity):
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 0}

    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/ressource.png'), (__class__.size, __class__.size))



class Animal(Entity):
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 1}
    movable = True

    def __init__(self, pos):
        super().__init__(pos)
        self.hitbox = Circle(pos, __class__.radius)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/animal.png'), (self.size, self.size))
        # for testing
        self.direction = VEC_2(math.sin(random.randint(0, 360) / math.pi), math.cos(random.randint(0, 360) / math.pi))
        

    def wander(self, dt):
        self.hitbox.pos += self.direction * dt * 20


    def run(self, dt):
        self.wander(dt)
        



class Structure(Entity):

    def __init__(self):
        super().__init__()


