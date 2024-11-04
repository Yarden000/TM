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
    Behavior,
    Steering
    )
from visualizing import(
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
        self.animal_list: list[Animal] = []
        self.movable_entity_list: list[Entity] = []
        self.animal_list: list[Animal] = []
        self.collision_detector = CollisionDetector()
        self.add_player()

        
        # for testing
        self.test_ents = [TestEntFood((-200, 100), self),
                          TestEntFood((0, 100), self),
                          TestEntFood((0, 300), self),
                          Animal((200, 200), self)
                          ]
        for ent in self.test_ents:
            self.spawn_ent(ent, overide=True)
        

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
        if ent.__class__ == Animal:
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
    
    def run_animals(self, dt) -> None:
        for ent in self.animal_list:
            ent.get_wants()
        for ent in self.animal_list:
            ent.change_vel()
        for ent in self.animal_list:
            ent.aply_vel(dt)
            ent.run(dt)

    def run(self, dt) -> None:
        '''runs all entity behaviours/interactions'''
        self.player.run(dt)
        self.run_animals(dt)
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


class Hitbox:
    '''base hotbox class'''
    kind = 'None'

    def __init__(self, pos: tuple[float | int, float | int] | VEC_2) -> None:
        self.pos = VEC_2(pos)
        self.color = 'blue'

    def scale(self, scalar) -> None:
        '''scales the hitbox by a scalar'''

    def rotate(self, angle) -> None:
        '''rotates the hitbox by an angle'''


class Rectangle(Hitbox):
    '''rectangular hitbox class'''
    kind = 'rect'

    def __init__(self, pos, angle, length, breadth) -> None:
        super().__init__(pos)
        self.angle = angle
        self.vec1 = VEC_2(math.cos(angle), math.sin(angle)) * length
        self.vec2 = VEC_2(math.sin(angle), -math.cos(angle)) * breadth

    def scale(self, scalar) -> None:
        self.vec1 = self.vec1 * scalar
        self.vec2 = self.vec2 * scalar

    def rotate(self, angle) -> None:
        self.angle += angle
        self.vec1 = self.vec1.rotate(angle)
        self.vec2 = self.vec2.rotate(angle)

    def draw(self, display_surface, displacement) -> None:
        '''draws the boundries of the hitbox'''
        pygame.draw.line(display_surface, self.color, displacement + self.pos + self.vec1 + self.vec2, displacement + self.pos + self.vec1 - self.vec2, width=1)
        pygame.draw.line(display_surface, self.color, displacement + self.pos - self.vec1 + self.vec2, displacement + self.pos - self.vec1 - self.vec2, width=1)
        pygame.draw.line(display_surface, self.color, displacement + self.pos + self.vec2 + self.vec1, displacement + self.pos + self.vec2 - self.vec1, width=1)
        pygame.draw.line(display_surface, self.color, displacement + self.pos - self.vec2 + self.vec1, displacement + self.pos - self.vec2 - self.vec1, width=1)


class Circle(Hitbox):
    '''circular hitbox class'''
    kind = 'circle'

    def __init__(self, center, radius) -> None:
        super().__init__(center)
        self.r = radius

    def scale(self, scalar) -> None:
        self.r = self.r * scalar

    def draw(self, display_surface, displacement) -> None:
        '''draws the boundries of the hitbox'''
        pygame.draw.circle(display_surface, self.color, displacement + self.pos, self.r, 1)


class Entity:
    '''class for all the enteties: ressouces, animals...'''

    spawning_rates = {'desert': 1, 'plains': 0.2, 'forest': 0}

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
    danger = 10
    max_speed = 50

    food = 1
    danger = 1
    
    def __init__(self, pos, entity_manager) -> None:
        self.visuals = []  # temporairy
        self.pos = VEC_2(pos)
        self.entity_manager = entity_manager
        self.ents_alrdy_coll_checked = [self]
        self.hitbox: Hitbox = Rectangle(pos, random.randint(0, 100) / 100000, self.radius, self.radius)  # the small angle helps with collision blocks
        self.region = tuple(self.hitbox.pos // self.entity_manager.region_size)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))

    def display(self, screen, displacement) -> None:
        '''displays the entity if it is on screen'''
        if -self.radius < self.hitbox.pos.x + displacement.x < WIDTH + self.radius:
            if -self.radius < self.hitbox.pos.y + displacement.y < HEIGHT + self.radius:
                screen.blit(self.image, self.image.get_rect(center=VEC_2(self.hitbox.pos + displacement)))

    def move(self, displacement) -> None:
        '''moves the entity'''
        self.hitbox.pos += displacement
        self.pos += displacement


class Ressource(Entity):
    '''resource class'''
    spawning_rates = {'desert': 0, 'plains': 1, 'forest': 0}
    image = pygame.image.load('../graphics/test/ressource.png')

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
    max_speed = 50 
    max_delta_v = 5

    def __init__(self, pos, entity_manager) -> None:
        super().__init__(pos, entity_manager)
        self.hitbox = Circle(pos, self.radius)
        Behavior.__init__(self, entitie_manager, self)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))

        # for testing
        self.vel = VEC_2()
        self.wanted_direction = None
        self.action = None

        self.behavior = Behavior(entity_manager, self)

        '''testing'''
        self.steering = Steering()
        self.player = self.entity_manager.player

    def get_wants(self) -> None:
        self.wanted_direction, self.action = self.behavior.wants()
        self.visuals.append(Line(self.pos, self.wanted_direction * 100, (0, 0, 200)))

    def change_vel(self) -> None:
        if self.wanted_direction:
            wanted_vel = self.wanted_direction * self.max_speed
        else:
            raise ValueError('no wanted direction')
        
        delta_v: VEC_2 = wanted_vel - self.vel
        if delta_v.magnitude() > self.max_delta_v:
            delta_v = delta_v.normalize() * self.max_delta_v
        
        self.vel += delta_v

    def aply_vel(self, dt) -> None:
        self.move(self.vel * dt)

    def run(self, dt) -> None:
        pass


class Player(Entity):
    '''player class'''
    movable = True
    image = pygame.image.load('../graphics/test/player.png')

    def __init__(self, camera, input_manager, entitie_manager) -> None:
        super().__init__((0, 0), entitie_manager)
        self.hitbox = Circle((0, 0), __class__.radius)
        self.velocity = VEC_2(0, 0)
        self.image = pygame.transform.scale(self.image.convert_alpha(), (self.size, self.size))
        self.speed = 100
        self.camera = camera
        self.input_manager = input_manager

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

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)
        self.hitbox = Circle(pos, 32)


class TestEntDanger(Entity):
    '''entity for testing behaviors'''
    collidable = False
    image = pygame.image.load('../graphics/test/redsphere.png')
    interests = {
        'food': 0,
        'danger': 50
        }

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)
        self.hitbox = Circle(pos, 32)


class TestEntMating(Entity):
    '''entity for testing behaviors'''
    collidable = False
    image = pygame.image.load('../graphics/test/purplesphere.png')

    def __init__(self, pos, entitie_manager) -> None:
        super().__init__(pos, entitie_manager)
        self.hitbox = Circle(pos, 32)