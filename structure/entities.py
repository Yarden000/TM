'''entities'''
import time
import random
import math
import pygame
from settings import (
    WIDTH,
    HEIGHT,
    VEC_2,
    PI
    )
from collisions import (
    CollisionDetector
)
from behaviors import (
    Geometries,
    Behavior,
    Steering,
    Sight
    )
from hitboxes import(
    Rectangle,
    Circle,
    Hitbox,
    DrawPoints,
    Line
)


class EntityManager:
    '''manages all the entitie interactions'''
    def __init__(self, input_manager, camera) -> None:
        self.camera = camera
        self.input_manager = input_manager
        self.regions: dict[tuple, list[Entity]] = {}
        self.region_size = 200  # needs to be bigger than all entity sizes
        self.entity_list: list[Entity] = []
        self.movable_entity_list: list[Entity] = []
        self.animal_list: list[Animal] = []
        self.collision_detector = CollisionDetector()
        self.add_player()

        
        self.spawn_ent(Animal(VEC_2(400, 0), self))
        self.spawn_ent(Ressource(VEC_2(200, -400), self))
        self.spawn_ent(Ressource(VEC_2(200, -200), self))
        '''
        self.spawn_ent(Ressource(VEC_2(200, -400), self))
        self.spawn_ent(Ressource(VEC_2(200, -300), self))
        self.spawn_ent(Ressource(VEC_2(200, -200), self))
        self.spawn_ent(Ressource(VEC_2(200, -100), self))
        self.spawn_ent(Ressource(VEC_2(200, 0), self))
        self.spawn_ent(Ressource(VEC_2(200, 100), self))
        self.spawn_ent(Ressource(VEC_2(200, 200), self))
        self.spawn_ent(Ressource(VEC_2(200, 300), self))
        self.spawn_ent(Ressource(VEC_2(200, 400), self))
        '''

    def add_player(self) -> None:
        '''creates the player'''
        self.player = Player(self.camera, self.input_manager, self)
        self.entity_list.append(self.player)
        self.movable_entity_list.append(self.player)
        self.player.region = (None, None)
        self.update_ent_region(self.player)

    def spawn_ent(self, ent, overide=False) -> None:
        '''creates an entity'''
        self.entity_list.append(ent)
        if ent.movable:
            self.movable_entity_list.append(ent)
        if isinstance(ent, Animal):
            self.animal_list.append(ent)
        ent.region = (None, None)
        self.update_ent_region(ent)
        # print(self.regions[ent.region])
        collision_state = self.entity_collision_state(ent, do_pushout=False)
        if collision_state and not overide:
            self.remove_entity(ent)

    def update_ent_region(self, entity) -> None:  # why doesn't it let entity: Entity
        '''updates the regions if an entity moved grom one region to another'''
        new_region = tuple(entity.hitbox.pos // self.region_size)
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
        region = tuple(self.player.hitbox.pos // self.region_size)
        dist = 5  # radius of regions checked
        n = 0
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.regions:
                    n += len(self.regions[region_])
        density = n / (((dist + 1) * self.region_size) * ((dist + 1) * self.region_size)) * 1000000   # the *100000 is because the density is very small
        return density

    def entity_collision_state(self, ent, do_pushout=False) -> bool:   # needs optimisation
        '''checks if an entity is colliding with any other entity and potentialy aplies the pushout'''
        collision_detected = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        if ent_ != ent:
                            if pushout := self.collision_detector.ent_ent_collision(ent.hitbox, ent_.hitbox):
                                if not do_pushout:
                                    return True
                                else:
                                    self.pushout(ent, ent_, pushout)
                                collision_detected = True
        return collision_detected

    def entity_collision_state_(self, ent, do_pushout=False) -> tuple[int, int]:  # temporary, just for testing optimisations
        '''checks if an entity is colliding with any other entity and potentialy aplies the pushout'''
        check_counter = 0
        skiped_counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                region = (ent.region[0] + i, ent.region[1] + j)
                if region in self.regions:
                    for ent_ in self.regions[region]:
                        if ent_ not in ent.ents_alrdy_coll_checked and ent_.collidable:
                            ent_.ents_alrdy_coll_checked.append(ent)
                            # print(ent, ent_)
                            check_counter += 1
                            if pushout := self.collision_detector.ent_ent_collision(ent.hitbox, ent_.hitbox):
                                ent.hitbox.color = 'red'
                                ent_.hitbox.color = 'red'
                                if do_pushout:
                                    self.pushout(ent, ent_, pushout)
                        else:
                            skiped_counter += 1
        return check_counter, skiped_counter

    def pushout(self, ent, ent_, dissplacement: VEC_2) -> None:
        '''aplies the pushout to the movable entity'''
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
                # print(ent.movable, ent_.movable)
                raise ValueError('Two imovable enteties are colliding')

    def colisions(self) -> None:
        '''aplies the collisions for all entities'''
        check_counter = 0
        skiped_counter = 0
        
        for ent in self.entity_list:
            if ent.collidable:
                c1, c2 = self.entity_collision_state_(ent, do_pushout=True)
                check_counter += c1
                skiped_counter += c2
                ent.ents_alrdy_coll_checked = [ent]
        # print(check_counter, skiped_counter)

    def remove_entity(self, ent) -> None:
        '''removes/kills an entity'''
        self.regions[ent.region].remove(ent)
        self.entity_list.remove(ent)
        if ent in self.movable_entity_list:
            self.movable_entity_list.remove(ent)
        if ent in self.animal_list:
            self.animal_list.remove(ent)
        del ent

    def run(self, dt) -> None:
        '''runs all entity behaviours/interactions'''
        self.player.run(dt)
        for ent in self.animal_list:
            ent.get_sight()
        for ent in self.entity_list:
            if not ent == self.player:
                ent.run(dt)
            else:  # debugging
                # print(tuple(self.player.pos // self.region_size))
                pass
        self.update_regions()
        '''testing'''
        self.colisions()
        
    def draw_regions(self, player_displacement: VEC_2) -> None:
        '''draws the region borders'''
        r = 20
        for i in range(-r, r + 1):
            k = i * self.region_size
            pygame.draw.line(pygame.display.get_surface(), 'red', VEC_2(-r * self.region_size, k) + player_displacement, VEC_2(r * self.region_size, k) + player_displacement)
            pygame.draw.line(pygame.display.get_surface(), 'red', VEC_2(k, -r * self.region_size) + player_displacement, VEC_2(k, r * self.region_size) + player_displacement)


class Entity:
    '''class for all the enteties: ressouces, animals...'''

    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 0}

    movable = False
    collidable = True
    opaque = True
    
    image = pygame.image.load('../graphics/test/none.png')

    size = 64
    radius = size / 2
    danger = 10
    max_speed = 50

    food = 1
    danger = 1
    
    def __init__(self, pos, entitie_manager) -> None:
        self.entitie_manager = entitie_manager
        self.ents_alrdy_coll_checked = [self]
        self.hitbox: Hitbox = Circle(pos, __class__.radius)
        #self.hitbox: Hitbox = Rectangle(pos, random.randint(0, 100) / 10000, self.radius, self.radius)  # the small angle helps with collision blocks
        
        '''to be able to visualize multiple hitboxes per entity'''
        self.other_hitboxes = {'obs_avoid': None, 'seeing_angle': None, 'important_points': DrawPoints(), 'lines': Line()}
        
        self.region = tuple(self.hitbox.pos // self.entitie_manager.region_size)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))

        self.vel = VEC_2(10, 0)

    def display(self, screen, camera) -> None:
        '''displays the entity if it is on screen'''
        if -self.radius < self.hitbox.pos.x + camera.player_displacement.x < WIDTH + self.radius:
            if -self.radius < self.hitbox.pos.y + camera.player_displacement.y < HEIGHT + self.radius:
                screen.blit(self.image, self.image.get_rect(center=VEC_2(self.hitbox.pos + camera.player_displacement)))

    def move(self, displacement) -> None:
        '''moves the entity'''
        self.hitbox.pos += displacement

    def run(self, dt) -> None:
        '''runs the behaviors'''


class Ressource(Entity):
    '''resource class'''
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 0}
    image = pygame.image.load('../graphics/test/ressource.png')

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))


class Plant(Ressource):
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 1}
    image = pygame.image.load('../graphics/test/plant.png')

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))


class Animal(Entity, Behavior):
    '''animal class'''
    spawning_rates = {'desert': 0, 'plains': 0, 'forest': 0.1}
    movable = True
    image = pygame.image.load('../graphics/test/animal.png')

    max_herd_size = 5
    herds:list[list] = []

    wander_angle = 0
    max_speed = 150
    max_satiation = 100
    max_hp = 100
    collision_avoidance_dist = 200

    def __init__(self, pos, entitie_manager) -> None:
        Entity.__init__(self, pos, entitie_manager)
        self.hitbox = Circle(pos, self.radius)
        Behavior.__init__(self, entitie_manager, self)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))

        '''testing'''
        self.player = self.entitie_manager.player
        self.sight = Sight(self)
        self.ents_seen:list = []

        self.curent_acktion = None
        self.satiation = self.max_satiation
        self.hp = self.max_hp

        # how much the animal considers another animal food or danger
        self.food_considerations:dict[object, float] = {
            Ressource: 10.1,
            Plant: 0.0,
            Animal: 0.01,
            Bunny: 5.0,
            Crock: 1.0
        }
        self.danger_considerations:dict[object, float] = {
            Ressource: 0.0,
            Plant: 0.0,
            Animal: 0.01,
            Bunny: 0.1,
            Crock: 10.0
        }

    def get_sight(self) -> None:
        self.ents_seen = self.sight.ents_seen()

    def get_want(self) -> None:
        pass

    def move_to_player(self, dt) -> None:
        '''temporairy'''
        # print(self.player.hitbox.pos)
        dv = self.steering.react(self, self.player.hitbox.pos, velocity = self.player.velocity, flee = False, stop_at = False)
        self.vel += dv * dt
        if self.vel.magnitude() <= self.max_speed:
            self.hitbox.pos += self.vel * dt
        else:
            self.hitbox.pos += self.vel.normalize() * self.max_speed * dt

    def run(self, dt) -> None:
        self.move_to_player(dt)

class Bunny(Animal):
    spawning_rates = {'desert': 0, 'plains': 0.1, 'forest': 0.1}
    image = pygame.image.load('../graphics/test/bunny.png')

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)

        # how much the animal considers another animal food or danger
        self.food_considerations:dict[object, float] = {
            Ressource: 0,
            Plant: 5,
            Animal: 0,
            Bunny: 0,
            Crock: 0
        }
        self.danger_considerations:dict[object, float] = {
            Ressource: 0,
            Plant: 0,
            Animal: 3,
            Bunny: 0.1,
            Crock: 10
        }

class Crock(Animal):
    spawning_rates = {'desert': 0, 'plains': 0.1, 'forest': 0.1}
    image = pygame.image.load('../graphics/test/crock.png')

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)

        # how much the animal considers another animal food or danger
        self.food_considerations:dict[object, float] = {
            Ressource: 0,
            Plant: 0,
            Animal: 1,
            Bunny: 5,
            Crock: 0.1
        }
        self.danger_considerations:dict[object, float] = {
            Ressource: 0,
            Plant: 0,
            Animal: 0.5,
            Bunny: 0.01,
            Crock: 10
        }

class Player(Entity):
    '''player class'''
    movable = True
    image = pygame.image.load('../graphics/test/player.png')

    def __init__(self, camera, input_manager, entitie_manager) -> None:
        super().__init__((0, 0), entitie_manager)
        # self.hitbox = Circle((0, 0), __class__.radius)
        self.velocity = VEC_2(0, 0)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))
        self.speed = 100
        self.camera = camera
        self.input_manager = input_manager

        # testing
        self.geometries = Geometries(32)

    def move(self, displacement) -> None:
        self.camera.player_displacement -= displacement
        self.camera.true_player_displacement -= displacement
        self.hitbox.pos += displacement

    def attack(self) -> None:
        '''temporairy'''
        click = self.input_manager.attack_click()
        if click is not None:
            angle = VEC_2(1, 0).angle_to(VEC_2(click) - self.hitbox.pos - self.camera.player_displacement) * PI / 180
            length = 100
            width = 50
            point = VEC_2(math.cos(angle), math.sin(angle)) * length
            rect = Rectangle(point - self.camera.true_player_displacement, angle, length, width)
            self.entitie_manager.spawn_ent(Attack(rect, self.entitie_manager), overide=True)

    def visualise_directions(self, display_surface) -> None:
        '''for testing'''
        directions = self.entitie_manager.set_player_geometrie()
        counter = 0
        vectors = []
        for direction in directions:
            color = 'green' if direction >= 0 else 'red'
            pos = VEC_2(WIDTH / 2, HEIGHT / 2)
            angle = (counter / len(directions)) * 2 * math.pi
            vector = VEC_2(100, 0).rotate(angle * 180 / math.pi) * 10 # * direction
            vectors.append(vector)
            vector_abs = VEC_2(100, 0).rotate(angle * 180 / math.pi) * 10 # * abs(direction)
            pygame.draw.line(display_surface, color, pos, pos + vector_abs, width=2)
            counter += 1
        weights_ = [vec.magnitude() for vec in vectors]
        chosen_vector = random.choices(vectors, weights=weights_, k=1)
        self.speed_vec += chosen_vector[0] * 0.1
        if self.speed_vec.magnitude() > self.speed:
            self.speed_vec = self.speed_vec.normalize() * self.speed

    def display(self, screen, camera) -> None:
        screen.blit(self.image, self.image.get_rect(center=(WIDTH/2, HEIGHT/2)))

    def run(self, dt) -> None:
        self.velocity = self.input_manager.player_movement() * self.speed
        self.move(self.velocity * dt)
        self.attack()


class Attack(Entity):
    '''base attack class'''
    collidable = False
    image = pygame.image.load('../graphics/test/flame.png')

    def __init__(self, hitbox: Rectangle, entitie_manager) -> None:
        super().__init__(hitbox.pos, entitie_manager)
        self.hitbox = hitbox
        self.image = pygame.transform.scale(self.image, (self.hitbox.vec1.magnitude() * 2, self.hitbox.vec2.magnitude() * 2))
        self.image = pygame.transform.rotate(self.image.convert_alpha(), -self.hitbox.angle * 180 / math.pi)
        self.spawn_time = time.time()
        self.stay_time = 0.5

    def move(self, displacement) -> None:
        self.hitbox.pos += displacement

    def kill(self) -> None:
        '''timer for the attack'''
        # print(time.time() - self.spawn_time)
        if time.time() - self.spawn_time > self.stay_time:
            # print(self.region)
            self.entitie_manager.remove_entity(self)
            # print(self)

    def do_damage(self) -> None:
        '''kills entities that tuch the attack'''
        region = tuple(self.hitbox.pos // self.entitie_manager.region_size)
        dist = 1
        enteties_hit = []
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.entitie_manager.regions:
                    # print(len(self.entityManager.regions[region_]))
                    for ent in self.entitie_manager.regions[region_]:
                        if ent.collidable:
                            # print(ent.hitbox.pos, ent.hitbox.vec1, ent.hitbox.vec2)
                            if self.entitie_manager.collision_detector.ent_ent_collision(self.hitbox, ent.hitbox):
                                # print(ent)
                                enteties_hit.append(ent)
        for ent in enteties_hit:
            # print(ent)
            if ent != self.entitie_manager.player:
                self.entitie_manager.remove_entity(ent)

    def run(self, dt) -> None:
        self.do_damage()
        self.kill()
