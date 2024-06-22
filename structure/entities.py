import pygame, sys, time
import random
import math
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    angle_between_vectors
    )
from attack import(
    Attack
    )
from collisions import(
    Collision_detector
)

class EntityManager:
    def __init__(self, input_manager, camera):
        self.camera = camera
        self.input_manager = input_manager
        self.regions = {}
        self.region_size = 200  # needs to be bigger than all entity sizes
        self.entity_list = []
        self.movable_entity_list = []
        self.collision_detector = Collision_detector()
        self.attack = Attack(self, camera)
        self.add_player()
        

    def add_player(self):
        self.player = Player(self.camera, self.input_manager, self)
        self.entity_list.append(self.player)
        self.movable_entity_list.append(self.player)
        self.player.region = None
        self.update_ent_region(self.player)
        
    def spawn_ent(self, ent, overide = False): 
        self.entity_list.append(ent)
        if ent.movable:
            self.movable_entity_list.append(ent)
        ent.region = None
        self.update_ent_region(ent)
        #print(self.regions[ent.region])
        collision_state = self.entity_collision_state(ent, do_pushout=False)
        if collision_state and not overide:
            self.remove_entity(ent)

    def update_ent_region(self, entity):
        new_region = tuple(entity.hitbox.pos // self.region_size)
        #print(entity.region, new_region)
        #print(self.regions[entity.region])
        if new_region != entity.region:
            if new_region in self.regions:
                self.regions[new_region].append(entity)
            else:
                self.regions[new_region] = [entity]
            if entity.region in self.regions:
                if entity in self.regions[entity.region]:
                    self.regions[entity.region].remove(entity)
            entity.region = new_region

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
        collision_detected = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        if ent_ != ent:
                            #print(ent, ent_)
                            collisionn_state, pushout = self.collision_detector.collision(ent.hitbox, ent_.hitbox)
                            if collisionn_state:
                                if not do_pushout:
                                    return True
                                else:
                                    '''if ent == self.player or ent_ == self.player:
                                        print(ent, ent_, pushout)'''
                                    self.pushout(ent, ent_, pushout)
                                collision_detected =  True
        return collision_detected
    
    def entity_collision_state_(self, ent, do_pushout=False):   # needs optimisation
        check_counter = 0
        skiped_counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        if (not ent_ in ent.ents_alrdy_coll_checked) and ent_.collidable:
                            ent_.ents_alrdy_coll_checked.append(ent)
                            #print(ent, ent_)
                            collisionn_state, pushout = self.collision_detector.collision(ent.hitbox, ent_.hitbox)
                            check_counter += 1
                            if collisionn_state:
                                ent.hitbox.color = 'red'
                                ent_.hitbox.color = 'red'
                                '''if ent == self.player or ent_ == self.player:
                                    print(ent, ent_, pushout)'''
                                self.pushout(ent, ent_, pushout)
                        else: skiped_counter += 1
        return check_counter, skiped_counter
    
    def pushout(self, ent, ent_, dissplacement):
        if ent.movable:
            if ent_.movable:
                ent.move(dissplacement / 2) 
                ent_.move(-dissplacement / 2) 
            else:
                ent.move(dissplacement) 
        else:
            if ent_.movable:
                ent_.move(-dissplacement) 
            else:
                #print(ent.movable, ent_.movable)
                raise ValueError('Two imovable enteties are colliding')
        
    def colisions(self):
        check_counter = 0
        skiped_counter = 0
        for ent in self.entity_list:
            ent.hitbox.color = 'blue'
        for ent in self.entity_list:
            if ent.collidable:
                c1, c2 = self.entity_collision_state_(ent, do_pushout=True) 
                check_counter += c1
                skiped_counter += c2
                ent.ents_alrdy_coll_checked = [ent]
        print(check_counter, skiped_counter)

    def remove_entity(self, ent):
        #print(ent)
        self.regions[ent.region].remove(ent)
        self.entity_list.remove(ent)
        if ent in self.movable_entity_list:
            self.movable_entity_list.remove(ent)
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
        start = time.time()
        self.colisions()
        end = time.time()
        #print((end - start) * 1000)

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
        self.color = 'blue'
        self.angle = angle
        self.vec1 = VEC_2(math.cos(angle), math.sin(angle)) * length
        self.vec2 = VEC_2(math.sin(angle), -math.cos(angle)) * breadth
        

    def scale(self, scalar):
        self.vectors[0] = self.vectors[0] * scalar
        self.vectors[1] = self.vectors[1] * scalar

    def rotate(self, angle):
        self.angle += angle
        self.vectors[0] = self.vectors[0].rotate(angle)
        self.vectors[1] = self.vectors[1].rotate(angle)
    
    def draw(self, display_surface, camera):
        #print(self.pos)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos + self.vec1 + self.vec2, camera.player_displacement + self.pos + self.vec1 - self.vec2, width = 1)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos - self.vec1 + self.vec2, camera.player_displacement + self.pos - self.vec1 - self.vec2, width = 1)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos + self.vec2 + self.vec1, camera.player_displacement + self.pos + self.vec2 - self.vec1, width = 1)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos - self.vec2 + self.vec1, camera.player_displacement + self.pos - self.vec2 - self.vec1, width = 1)

class Circle(Hitbox):
    kind = 'circle'

    def __init__(self, center, radius):
        super().__init__(center)
        self.color = 'blue'
        self.r = radius

    def scale(self, scalar):
        self.r = self.r * scalar

    def draw(self, display_surface, camera):
        pygame.draw.circle(display_surface, self.color, camera.player_displacement + self.pos, self.r, 1)


class Entity:
    # class for all the enteties: ressouces, animals...
    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 0}
    movable = False
    collidable = True
    size = 64
    radius = size / 2

    def __init__(self, pos, entitie_manager):
        self.entitie_manager = entitie_manager
        self.ents_alrdy_coll_checked = [self]
        self.hitbox = Rectangle(pos, random.randint(0, 100) / 100000, __class__.radius, __class__.radius) # the small angle helps with collision blocks
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

    def __init__(self, pos, entitie_manager):
        super().__init__(pos, entitie_manager)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/ressource.png'), (__class__.size, __class__.size))


class Animal(Entity):
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 1}
    movable = True

    def __init__(self, pos, entitie_manager):
        super().__init__(pos, entitie_manager)
        self.hitbox = Circle(pos, __class__.radius)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/animal.png'), (self.size, self.size))
        # for testing
        angle = random.randint(0, 360)
        self.direction = VEC_2(math.sin(angle / math.pi), math.cos(angle / math.pi))
        

    def wander(self, dt):
        self.hitbox.pos += self.direction * dt * 100


    def run(self, dt):
        self.wander(dt)
        

class Player(Entity):
    movable = True
    def __init__(self, camera, input_manager, entitie_manager):
        super().__init__((0, 0), entitie_manager)
        #self.hitbox = Circle((0, 0), __class__.radius)
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/player.png'), (self.size, self.size))
        self.speed = 100
        self.camera = camera
        self.input_manager = input_manager
        

    def move(self, displacement):
        self.camera.player_displacement -= displacement
        self.camera.true_player_displacement -= displacement
        self.hitbox.pos += displacement

    def attack(self):
        click = self.input_manager.attack_click()
        if click != None:
            angle = -angle_between_vectors(VEC_2(1, 0), VEC_2(click) - self.hitbox.pos - self.camera.player_displacement)
            length = 100
            width = 50
            point = VEC_2(math.cos(angle), math.sin(angle)) * length
            rect = Rectangle(point - self.camera.true_player_displacement, angle, length, width)
            #print(rect.pos, rect.vec1, rect.vec2)
            #self.attack.rect_attack(rect)       
            self.entitie_manager.spawn_ent(Attack_(rect, self.entitie_manager), overide = True)

    

    def display(self, screen, camera):
        screen.blit(self.image, self.image.get_rect(center = (WIDTH/2, HEIGHT/2)))

    def run(self, dt):
        self.move(self.input_manager.player_movement() * dt * self.speed)
        self.attack()
        


class Attack_(Entity):
    collidable = False
    def __init__(self, hitbox, entitie_manager):
        super().__init__(hitbox.pos, entitie_manager)
        self.hitbox = hitbox
        self.image = pygame.transform.scale(pygame.image.load('../graphics/test/flame.png'), (self.hitbox.vec1.magnitude() * 2, self.hitbox.vec2.magnitude() * 2))
        self.image = pygame.transform.rotate(self.image, -self.hitbox.angle * 180 / math.pi)
        self.spawn_time = time.time()
        self.stay_time = 0.5

    def move(self, displacement):
        self.hitbox.pos += displacement

    def kill(self):
        #print(time.time() - self.spawn_time)
        if time.time() - self.spawn_time > self.stay_time:
            #print(self.region)
            self.entitie_manager.remove_entity(self)
            #print(self)

    def do_damage(self):
        region = tuple(self.hitbox.pos // self.entitie_manager.region_size)
        dist = 1
        enteties_hit = []
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.entitie_manager.regions:
                    #print(len(self.entityManager.regions[region_]))
                    for ent in self.entitie_manager.regions[region_]:
                        if ent.collidable:
                            #print(ent.hitbox.pos, ent.hitbox.vec1, ent.hitbox.vec2)
                            collision_state, poushout = self.entitie_manager.collision_detector.collision(self.hitbox, ent.hitbox)
                            if collision_state:
                                #print(ent)
                                enteties_hit.append(ent)
        for ent in enteties_hit: 
            #print(ent)
            if ent != self.entitie_manager.player:
                self.entitie_manager.remove_entity(ent) 

    def run(self, dt):
        self.do_damage()
        self.kill()

class Structure(Entity):

    def __init__(self):
        super().__init__()


