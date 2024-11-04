'''entities'''
import time
import random
import math
import pygame
import pymunk
from settings import (
    WIDTH,
    HEIGHT,
    VEC_2,
    PY_VEC_2,
    PI
    )

from behaviors import (
    Behavior,
    Steering,
    Sight
    )



class EntityManager:
    '''manages all the entitie interactions'''
    def __init__(self, input_manager, camera) -> None:
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.camera = camera
        self.input_manager = input_manager
        self.regions: dict[tuple, list[Entity]] = {}
        self.region_size = 200  # needs to be bigger than all entity sizes
        self.entity_list: list[Entity] = []
        self.animal_list: list[Animal] = []
        self.movable_entity_list: list[Entity] = []
        self.animal_list: list[Animal] = []
        self.add_player()
        # for testing
        self.test_ents = [TestEntFood((-200, 100), self),
                          TestEntFood((0, 100), self),
                          TestEntFood((0, 300), self),
                          Animal((200, 200), self)
                          ]
        for ent in self.test_ents:
            self.spawn_ent(ent, overide=True)

        self.remove_collisions_with_attacks()
    
    def col_detect(self, ent):
        # Check if the new shape overlaps with any existing shape
        if self.space.shape_query(ent.shape):
            return True
        return False
    
    def remove_collisions_with_attacks(self):
        handler = self.space.add_collision_handler(1, 3)

        def f(arbirer, space, data):
            return False
        
        handler.pre_solve = f

    def add_player(self) -> None:
        '''creates the player'''
        self.player = Player(self.camera, self.input_manager, self)
        self.entity_list.append(self.player)
        self.movable_entity_list.append(self.player)
        self.player.region = (None, None)
        self.update_ent_region(self.player)
        self.space.add(self.player.body, self.player.shape)
        
    def spawn_ent(self, ent, overide=False) -> None:
        '''creates an entity'''
        
        if not (overide or (not self.col_detect(ent))):
            self.remove_entity(ent)
            print('hbF')
        else: 
            
            self.entity_list.append(ent)
            if ent.movable:
                self.movable_entity_list.append(ent)
            if isinstance(ent, Animal):
                self.animal_list.append(ent)
            ent.region = (None, None)
            self.update_ent_region(ent)
            self.space.add(ent.body, ent.shape)


        '''
        collision_state = self.entity_collision_state(ent, do_pushout=False)
        if collision_state and not overide:
            self.remove_entity(ent)
        '''
    def update_ent_region(self, entity) -> None:  # why doesn't it let entity: Entity
        '''updates the regions if an entity moved grom one region to another'''
        new_region = tuple(entity.body.position // self.region_size)
        # print(entity.region, new_region)
        # print(self.regions[entity.region])
        if new_region != entity.region:
            if new_region in self.regions:
                self.regions[new_region].append(entity)
            else:
                self.regions[new_region] = [entity]
            if entity.region in self.regions:
                if entity in self.regions[entity.region]:
                    self.regions[entity.region].remove(entity)
            entity.region = new_region

    def update_regions(self) -> None:
        '''updates the regions for alkl entities'''
        for ent in self.movable_entity_list:
            self.update_ent_region(ent)

    def ent_density(self) -> float:
        '''calculates the density of entities arround the player'''
        region = tuple(self.player.body.position // self.region_size)
        dist = 5  # radius of regions checked
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.regions:
                    n += len(self.regions[region_])
        density = n / (((dist + 1) * self.region_size) * ((dist + 1) * self.region_size)) * 1000000   # the *100000 is because the density is very small
        return density
    
    def remove_entity(self, ent) -> None:
        '''removes/kills an entity'''
        if ent.body in self.space.bodies:
            self.space.remove(ent.body)
        if ent.shape in self.space.shapes:
            self.space.remove(ent.shape)
        if ent.region in self.regions:
            if ent in self.regions[ent.region]:
                self.regions[ent.region].remove(ent)
        if ent in self.entity_list:
            self.entity_list.remove(ent)
        if ent in self.movable_entity_list:
            self.movable_entity_list.remove(ent)
        if ent in self.animal_list:
            self.animal_list.remove(ent)
        del ent
    
    def run_animals(self, dt) -> None:
        for ent in self.animal_list:
            ent.get_wants()
        for ent in self.animal_list:
            ent.change_vel(dt)
        for ent in self.animal_list:
            ent.run(dt)

    def run(self, dt) -> None:
        '''runs all entity behaviours/interactions'''
        self.player.run(dt)
        # self.run_animals(dt)
        self.update_regions()
        '''testing'''
        self.space.step(dt)
        self.player.displace_after_colisions()
        
    def draw_regions(self, player_displacement: VEC_2) -> None:
        '''draws the region borders'''
        r = 20
        for i in range(-r, r + 1):
            k = i * self.region_size
            pygame.draw.line(pygame.display.get_surface(), 'red', VEC_2(-r * self.region_size, k) + player_displacement, VEC_2(r * self.region_size, k) + player_displacement)
            pygame.draw.line(pygame.display.get_surface(), 'red', VEC_2(k, -r * self.region_size) + player_displacement, VEC_2(k, r * self.region_size) + player_displacement)


class Entity:
    '''class for all the enteties: ressouces, animals...'''

    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 100}

    movable = False
    collidable = True
    opaque = True
    
    image = pygame.image.load('../graphics/test/none.png')

    size = 64
    radius = size / 2
    interests = {
        'food': 0,
        'danger': 0
        }
    max_speed = 50

    food = 1
    danger = 1
    
    hitbox_shape = 'rect'
    body_type = pymunk.Body.DYNAMIC  # can be DYNAMIC, KINEMATIC, or STATIC view: https://www.pymunk.org/en/latest/pymunk.html#pymunk.Body
    collision_type = 1  # normal colision type

    def __init__(self, pos, entitie_manager) -> None:
        self.entity_manager = entitie_manager
        
        self.set_hitbox(pos)

        self.region = tuple(self.body.position // self.entity_manager.region_size)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))

        self.body.velocity = pymunk.Vec2d(10, 0)

    def set_hitbox(self, pos) -> None:
        self.body = pymunk.Body(1, float('inf'), self.body_type)
        self.body.position = (tuple(pos))
        if self.hitbox_shape == 'rect':
            self.shape = pymunk.Poly.create_box(self.body, (self.size, self.size))
        elif self.hitbox_shape == 'circle':
            self.shape = pymunk.Circle(self.body, self.radius)
        else:
            raise ValueError('unknown hitbox shape')
        self.shape.collision_type = self.collision_type
        self.shape.owner = self
        self.shape.elasticity = 0

    def display(self, screen, displacement) -> None:
        '''displays the entity if it is on screen'''
        if -self.radius < self.body.position.x + displacement.x < WIDTH + self.radius:
            if -self.radius < self.body.position.y + displacement.y < HEIGHT + self.radius:
                screen.blit(self.image, self.image.get_rect(center=VEC_2(self.body.position + displacement)))

    def move(self, displacement) -> None:
        '''moves the entity'''
        self.body.position += displacement

    def run(self, dt) -> None:
        '''runs the behaviors'''

    def kill(self):
        self.entity_manager.remove_entity(self)



class Ressource(Entity):
    '''resource class'''
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 0}
    image = pygame.image.load('../graphics/test/ressource.png')
    body_type = pymunk.Body.STATIC

    def __init__(self, pos, entity_manager) -> None:
        super().__init__(pos, entity_manager)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))


class Plant(Ressource):
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 1}
    image = pygame.image.load('../graphics/test/plant.png')

    def __init__(self, pos, entity_manager) -> None:
        super().__init__(pos, entity_manager)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))


class Animal(Entity):
    '''animal class'''
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 0.1}
    movable = True
    image = pygame.image.load('../graphics/test/animal.png')
    hitbox_shape = 'circle'

    wander_angle = 0
    max_speed = 100
    max_delta_v = 200
    max_satiation = 100
    max_hp = 100
    collision_avoidance_dist = 200
    

    def __init__(self, pos, entity_manager) -> None:
        super().__init__(pos, entity_manager)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))

        # for testing
        self.vel = VEC_2()
        self.wanted_direction = None
        self.action = None

        self.behavior = Behavior(entity_manager, self)
        
        self.ents_seen:list = []

        self.curent_acktion = None
        self.satiation = self.max_satiation
        self.hp = self.max_hp

        self.body.velocity = pymunk.Vec2d(100, 0).rotated_degrees(random.randrange(0, 360))


    def get_wants(self) -> None:
        self.wanted_direction, self.action = self.behavior.wants()

    def change_vel(self, dt) -> None:
        if self.wanted_direction:
            wanted_vel = self.wanted_direction * self.max_speed
        else:
            raise ValueError('no wanted direction')
        
        delta_v: PY_VEC_2 = wanted_vel - self.vel
        if delta_v.length > self.max_delta_v:
            delta_v = delta_v.normalized() * self.max_delta_v
        
        self.body.velocity += delta_v * dt

        # friction
        self.body.velocity *= 1- 0.1 * dt

    def run(self, dt) -> None:
        pass

class Bunny(Animal):
    spawning_rates = {'desert': 0, 'plains': 0.1, 'forest': 0.1}
    image = pygame.image.load('../graphics/test/bunny.png')

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)


class Crock(Animal):
    spawning_rates = {'desert': 0, 'plains': 0.1, 'forest': 0.1}
    image = pygame.image.load('../graphics/test/crock.png')
    

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)


class Player(Entity):
    '''player class'''
    movable = True
    image = pygame.image.load('../graphics/test/player.png')

    def __init__(self, camera, input_manager, entitie_manager) -> None:
        super().__init__((0, 0), entitie_manager)
        self.body.velocity = pymunk.Vec2d(0, 0)
        self.body.mass = 1000
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))
        self.speed = 100
        self.camera = camera
        self.input_manager = input_manager

    def move(self, displacement) -> None:
        self.camera.player_displacement -= displacement
        self.camera.true_player_displacement -= displacement
        self.body.position += displacement
        self.previous_pos = self.body.position

    def displace_after_colisions(self):
        '''needed becausr during collision plase the camera displacement isn't adjusted'''
        displacement = self.body.position - self.previous_pos
        self.camera.player_displacement -= displacement
        self.camera.true_player_displacement -= displacement
        self.previous_pos += displacement

    def set_attack_hitbox(self, pos, angle, dimentions:tuple) -> tuple:
        body = pymunk.Body(1, float('inf'), pymunk.Body.STATIC)
        body.position = (tuple(pos))
        angle_in_rad = angle / math.pi * 180
        body.angle = angle_in_rad
        shape = pymunk.Poly.create_box(body, dimentions)
        shape.collision_type = 3
        return body, shape

    def attack(self) -> None:
        '''temporairy'''
        click = self.input_manager.attack_click()
        if click is not None:
            angle = VEC_2(1, 0).angle_to(VEC_2(click) - self.body.position - self.camera.player_displacement) * PI / 180
            length = 100
            width = 50
            point = pymunk.Vec2d(math.cos(angle), math.sin(angle)) * length
            pos = self.body.position + point
            body, shape = self.set_attack_hitbox(pos, angle, (width, length))
            self.entity_manager.spawn_ent(Attack(body, shape, (length, width), angle, self.entity_manager), overide=True)

    def display(self, screen, camera) -> None:
        screen.blit(self.image, self.image.get_rect(center=((WIDTH/2, HEIGHT/2))))

    def run(self, dt) -> None:
        self.body.velocity = self.input_manager.player_movement() * self.speed
        self.move(self.body.velocity * dt)
        self.attack()


class Attack(Entity):
    '''base attack class'''
    collidable = False
    image = pygame.image.load('../graphics/test/flame.png')

    collision_type = 3

    def __init__(self, body, shape, dimentions, angle, entitie_manager) -> None:
        super().__init__(body.position, entitie_manager)
        self.image = pygame.transform.scale(self.image, (dimentions[0] * 2, dimentions[1] * 2))
        self.image = pygame.transform.rotate(self.image.convert_alpha(), -angle * 180 / math.pi)
        self.spawn_time = time.time()
        self.stay_time = 0.5
        self.body = body
        self.shape = shape
        self.shape.owner = self

    def kill(self) -> None:
        '''timer for the attack'''
        # print(time.time() - self.spawn_time)
        if time.time() - self.spawn_time > self.stay_time:
            # print(self.region)
            self.entity_manager.remove_entity(self)
            # print(self)

    def do_damage(self):
        if infos := self.entity_manager.space.shape_query(self.shape):
            for info in infos:
                ent = info.shape.owner
                if ent is not self.entity_manager.player:
                    if ent.__class__ is not Attack:
                        ent.kill()

    def run(self, dt) -> None:
        self.do_damage()
        self.kill()


class Structure(Entity):
    '''base structure class'''


class TestEntFood(Entity):
    '''entity for testing behaviors'''
    collidable = False
    image = pygame.image.load('../graphics/test/bluesphere.png')
    interests = {
        'food': 50,
        'danger': 0
        }
    body_type = pymunk.Body.STATIC

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)


class TestEntDanger(Entity):
    '''entity for testing behaviors'''
    collidable = False
    image = pygame.image.load('../graphics/test/redsphere.png')
    interests = {
        'food': 0,
        'danger': 50
        }
    body_type = pymunk.Body.STATIC

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)


class TestEntMating(Entity):
    '''entity for testing behaviors'''
    collidable = False
    image = pygame.image.load('../graphics/test/purplesphere.png')
    body_type = pymunk.Body.STATIC

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)
