
import random
import math
from settings import (
    VEC_2,
    angle_between_vectors_0_to_2pi,
    angle_between_vectors_plus_minus_pi, 
    PI,
    debug_info
)
from hitboxes import (
    Rectangle, 
    DrawAngle,
    Line
)

class Behavior:
    '''where all the behavior calculations are done'''
    def __init__(self, entity_manager, ent) -> None:
        self.entity_manager = entity_manager
        self.entity = ent
        self.sight = Sight(ent)
        self.Geometries = Geometries(16)
        self.ActivationFunctions = ActivationFunctions()
        self.Averages = Averages()
        self.steering = Steering()
        self.collision_avoidance_handler = CollisionAvoidanceHandler()

    def vec(self, ent) -> VEC_2:
        return ent.hitbox.pos - self.entity.hitbox.pos
    
    def ent_food(self, ent) -> float:
        '''how much potential food an entity poses to self.ent'''
        # needs to take into account the ent's danger
        return self.entity.food_considerations[ent.__class__] * ent.food
    
    def ent_danger(self, ent) -> float:
        '''how much danger an entity poses to self.ent'''
        return self.entity.danger_considerations[ent.__class__]
    
    def ent_importance(self, ent, average_direction) -> float:
        '''how good/important an ent is(in relation to food or danger), (allignment with other food, ...)'''
        vec = self.vec(ent)
        angle = (vec).angle_to(average_direction) * PI / 180
        directional_compability = math.cos(angle) * 0.5 + 1
        print('directional_compability ', directional_compability)
        print('angle ', angle)
        return directional_compability / vec.magnitude() ** (1 / 4)

    def best_food(self, entity_list) -> tuple[object, float, VEC_2|None]|None:
        '''needs optimisation: vec(ent) and weight(ent) are calculated twice'''
        ent_list = [ent[0] for ent in entity_list if ent[0].__class__ in self.entity.food_considerations]

        if not ent_list:
            return None
        
        average_food_direction = self.Averages.average_vector(0.5,
                                                              [self.vec(ent) for ent in ent_list],
                                                              [self.ent_food(ent) for ent in ent_list])
        best_food = max(ent_list, key=lambda ent:self.ent_importance(ent, average_food_direction) * self.ent_food(ent), default = None)
        '''testing'''
        counter = 0
        ent_list.sort(key = lambda ent:ent.hitbox.pos.y)
        for ent in ent_list:
            counter += 1
            debug_info.append((' ent number ' + str(counter) +' : ' + str(self.ent_importance(ent, average_food_direction) * self.ent_food(ent)),
                               30 * counter, 10))
        return (best_food,
                self.ent_importance(best_food, average_food_direction) * self.ent_food(best_food),
                average_food_direction)
        
    
    def danger_direction(self, entity_list) -> tuple[VEC_2, float]|None:
        '''the direction where there is the most danger'''
        ent_list = [ent[0] for ent in entity_list if ent[0].__class__ in self.entity.danger_considerations]

        if not ent_list:
            return None
        
        average_danger_direction = self.Averages.average_vector(0.5,
                                                                [self.vec(ent) for ent in ent_list],
                                                                [self.ent_danger(ent) for ent in ent_list])
        vecs = []
        weights = []
        total_danger:float = 0
        for ent in ent_list:
            vecs.append(self.vec(ent).normalize())
            weight = self.ent_importance(ent, average_danger_direction) * self.ent_danger(ent)
            weights.append(weight)
            total_danger += weight
        
        if fleeing_direction := self.Averages.average_vector(1, vecs, weights):
            return (-fleeing_direction, total_danger)
        return None

    def combining_wants(self):
        ents_seen, angles = self.sight.ents_seen(want_angles=True)  # angles is for visualization^
        self.entity.other_hitboxes['seeing_angle'] = DrawAngle(self.entity.hitbox.pos, angles)

        player = self.entity_manager.player

        wants:list[dict] = []  # all the active behaviors, like chasing, fleeing, ...

        fleeing_direction, danger_amount, best_food, food_amount, food_direction = None, None, None, None, None
        if tmp := self.best_food(ents_seen):
            best_food, food_amount, average_food_direction = tmp
            food_direction = self.steering.react(self.entity, best_food.hitbox.pos, best_food.vel)
        if tmp := self.danger_direction(ents_seen):
            fleeing_direction, danger_amount = tmp

        food_strength = 1 / (self.entity.satiation / self.entity.max_satiation) * food_amount
        danger_strength = ((self.entity.hp / self.entity.max_hp - 1) ** 4 * 9 + 1) * danger_amount
        wander_strength = self.entity.satiation / self.entity.max_satiation / 2 + 0.5
        # heard_strength ...
        # mate_strengtg ...

        state = self.entity.curent_state
        if state == 'chasing_food':
            pass
        elif state == 'fleeing_danger':
            pass
        elif state == 'wandering':
            pass
        elif state == 'resting':
            pass

        # print('food :', best_food, food_amount)
        # print('danger :', fleeing_direction, danger_amount)

        self.entity.other_hitboxes['lines'].clear()
        if fleeing_direction:
            self.entity.other_hitboxes['lines'].add(self.entity.hitbox.pos, self.entity.hitbox.pos + fleeing_direction * 100, 'red', 5)
        if food_direction:
            self.entity.other_hitboxes['lines'].add(self.entity.hitbox.pos, self.entity.hitbox.pos + food_direction * 100, 'green', 5) 
        if average_food_direction:
            self.entity.other_hitboxes['lines'].add(self.entity.hitbox.pos, self.entity.hitbox.pos + average_food_direction * 100, 'purple', 5)
        return (VEC_2())
        '''
        food_list:list[tuple[VEC_2, float]] = []
        danger_list:list[tuple[VEC_2, float]] = []

        reaction = False
        for ent, dist in ents_seen:
            if ent.__class__ in self.entity.considerations:
                reaction = True

                food = self.entity.considerations[ent.__class__][0] * ent.food
                danger = self.entity.considerations[ent.__class__][1] * ent.danger

                dist_vec = self.entity.hitbox.pos - ent.hitbox.pos

                food_list.append((dist_vec, food))
                danger_list.append((dist_vec, danger))

        if reaction:
            food_vec_list = [food_[0] for food_ in food_list]
            food_weight_list = [food_[1] for food_ in food_list]
            danger_vec_list = [danger_[0] for danger_ in danger_list]
            danger_weight_list = [danger_[1] for danger_ in danger_list]

            average_food_direction:VEC_2 = self.Averages.average_vector(0.5, food_vec_list, food_weight_list)  # average of food_vec_list, number should be in genes
            average_danger_direction:VEC_2 = -self.Averages.average_vector(0.5, danger_vec_list, danger_weight_list)
            

            def f(food, direction) -> float:
                vec = food[0]
                amount = food[1]
                angle = (vec).angle_to(direction) * PI / 180
                directional_compability = math.cos(angle / 3)
                return directional_compability / vec.magnitude() ** (1 / 4) * amount
            
            mostimportant_food = max(food_list, key = lambda food_: f(food_, average_food_direction))[0]

            go_to_food = self.steering.react(self.entity, mostimportant_food, velocity = VEC_2(), flee = False, stop_at = True)
            

            self.entity.other_hitboxes['lines'].clear()
            for vec in danger_vec_list:
                self.entity.other_hitboxes['lines'].add(self.entity.hitbox.pos, self.entity.hitbox.pos + vec.normalize() * 100, 'purple', 10)
            self.entity.other_hitboxes['lines'].add(self.entity.hitbox.pos, self.entity.hitbox.pos + go_to_food * 100, 'green', 5)
            self.entity.other_hitboxes['lines'].add(self.entity.hitbox.pos, self.entity.hitbox.pos + average_food_direction.normalize() * 100, 'red', 5)
            #self.entity.other_hitboxes['line_2'] = Line(self.entity.hitbox.pos, self.entity.hitbox.pos + average_danger_direction * 100, 'red')
        '''

        '''go to player'''
        def in_tuple_list(list, x):
            for tuple_ in list:
                if x in tuple_:
                    return True
            return False
        if in_tuple_list(ents_seen, player):
            react_to_player = self.steering.react(self.entity, player.hitbox.pos, velocity = player.vel, flee = False, stop_at = True)
            dist = (self.entity.hitbox.pos - player.hitbox.pos).magnitude()
            wants.append({'direction': react_to_player, 'dist': dist, 'weight': 1})
            # testing
            self.entity.hitbox.color = 'purple'


        wandering = self.steering.wander_1(self.entity)
        wants.append({'direction': wandering, 'weight': 1})

        if grav_center := self.steering.grav_center(self.entity, ents_seen, self.ActivationFunctions.f3):
            wants.append({'direction': grav_center, 'weight': 0.1})

        def f(x):
            return x['weight']
        most_important_want = max(wants, key=f, default=None)

        if most_important_want:
            if 'dist' in most_important_want:
                dist = most_important_want['dist']
            else:
                dist = None
            want = self.collision_avoidance_handler.avoid_collision(self.entity, most_important_want['direction'], ents_seen, dist)

            '''visualisation'''
            # self.entity.other_hitboxes['line_1'] = Line(self.entity.hitbox.pos, self.entity.hitbox.pos + most_important_want['direction'] * 100, 'red')
            # self.entity.other_hitboxes['line_2'] = Line(self.entity.hitbox.pos, self.entity.hitbox.pos + want * 100, 'green')

            # self.entity.other_hitboxes['line_2'] = Line(self.entity.hitbox.pos, self.entity.hitbox.pos + want * 100, 'green')

        return want

        
class CollisionAvoidanceHandler:

    def __init__(self) -> None:
        self.angular_range_handeler = AngularRangeHandeler()

    def circle_circle(self, circle_1, circle_2) -> tuple[float, float]|None:
        '''returns the minimum and maximum angles to
        avoid a collision between two circles'''

        dist = (circle_1.pos - circle_2.pos).magnitude()
        temp = (circle_1.r + circle_2.r) / dist
        angle = -(circle_2.pos - circle_1.pos).angle_to(VEC_2(1, 0)) * PI / 180

        if temp > 1:
            beta = PI * 2 / 3
            return (angle - beta, angle + beta)

        alpha = math.asin(temp)
        return (angle - alpha, angle + alpha)
    
    def circle_rect(self, circle, rect, invert:bool=False) -> tuple[float, float]|None:
        '''returns the minimum and maximum angles to
        avoid a collision between a circle and a rect'''

        dist = (circle.pos - rect.pos).magnitude()

        return [0, 9.49]

    def rect_rect(self, rect_1, rect_2) -> tuple[float, float]|None:
        '''returns the minimum and maximum angles to
        avoid a collision between two rects'''

        dist = (rect_1.pos - rect_2.pos).magnitude()

        return [0, 9.49]
    
    def avoid_collision(self, ent, ent_want:VEC_2, ent_list:list, distance:float|None=None) -> VEC_2:
        '''returns the minimum and maximum angles to
        avoid a collision between two rects'''
        self.angular_range_handeler.clear()
        ent_hitbox = ent.hitbox

        '''testing'''

        def in_tuple_list(list, x):
            for tuple_ in list:
                if x in tuple_:
                    return tuple_
            return False
        if temp := in_tuple_list(ent_list, ent.entity_manager.player):
            ent_list.remove(temp)


        for entity, dist in ent_list:
            if distance and dist <= distance:
                if ent_hitbox.kind == 'circle':

                    if entity.hitbox.kind == 'circle':

                        if ang_range := self.circle_circle(ent_hitbox, entity.hitbox):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return VEC_2()
                        
                    else:

                        if ang_range := self.circle_rect(ent_hitbox, entity.hitbox):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return VEC_2()
                        
                else:

                    if entity.hitbox.kind == 'circle':

                        if ang_range := self.circle_rect(entity.hitbox, ent_hitbox, invert = True):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return VEC_2()
                        
                    else:

                        if ang_range := self.rect_rect(ent_hitbox, entity.hitbox):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return VEC_2()
                    
        #ent.other_hitboxes['seeing_angle'] = DrawAngle(ent.hitbox.pos, self.angular_range_handeler.ranges_list)

        angle = VEC_2().angle_to(ent_want) * PI / 180
        if angles := self.angular_range_handeler.borders(angle):
            #print(angles)
            v1 = VEC_2(1, 0).rotate_rad(angles[0])
            v2 = VEC_2(1, 0).rotate_rad(angles[1])
            def f(x:VEC_2):
                return x.dot(ent_want)
            best_direction = max([v1, v2], key = f)
            
            # print('react')
            return best_direction * ent_want.magnitude()
        # print('ignore')
        return ent_want


class HerdHandler:

    def __init__(self) -> None:
        self.Averages = Averages()

        self.all_herds:dict = {}
        self.lone_ents:dict = {}

    def rearange(self) -> None:
        self.clean_herds()
        self.aglomerate()

    def add_lone_ent(self, ent) -> None:
        ent_class = ent.__class__
        if ent_class in self.lone_ents:
            self.lone_ents[ent_class].append(ent)
        else:
            self.lone_ents[ent_class] = [ent]

    def clean_herds(self) -> None:
        for _class in self.all_herds:
            for herd in _class:
                self.expel_ents(herd)

    def expel_ents(self, herd) -> None:
        center = self.Averages.average_vector(0, [ent.hitbox.pos for ent in herd])

        def dist(x):
            return (center - x.hitbox.pos).magnitude_squared()

        farthest_ent = max(herd, key = dist)

        if dist(farthest_ent) > 500:  # need to be changed
            herd.remove(farthest_ent)
            self.add_lone_ent(farthest_ent)

            self.expel_ents(herd)

    def aglomerate(self) -> None:
        for _class in self.lone_ents:
            for ent in _class:
                pass


                    
                


class Herd:

    def __init__(self, entities:list):
        self.entities = entities


class Steering:

    def __init__(self) -> None:
        self.slowing_distance = 200
        self.collision_avoidance_handeler = CollisionAvoidanceHandler()

    def max_delta_v(self, norm, angle=0):  # angle is in refrence to f^direction
        '''
        is possible to add a geometry
        example https://www.red3d.com/cwr/steer/gdc99/ figure 2
        '''
        return 100 if norm > 100 else norm

    def leading_the_target(self, p1:VEC_2, v1:VEC_2, p2:VEC_2, s2:float, max_trailing:float=1.0) -> VEC_2:
        if v1.magnitude() == 0:
            return p1
        dist_vect = p2 - p1
        d = dist_vect.magnitude()
        s1 = v1.magnitude()
        alpha = angle_between_vectors_0_to_2pi(dist_vect, v1)

        tmp = math.sin(alpha) * s1 / s2

        # there is no trajectory where p2 interceps p1
        if tmp > 1:
            tmp = 1
        elif tmp < -1:
            tmp = -1

        beta = math.asin(tmp)

        delta = math.pi - alpha - beta

        t = math.sin(alpha) * d / (s2 * math.sin(delta)) if abs(delta) > 0.00001 else 10000
        t = abs(t)
        
        if t > d * max_trailing:
            t = d * max_trailing
        
        p3 = p1 + t * v1

        return p3
  
    def react(self, entity, point:VEC_2, velocity:VEC_2|None=None, flee:bool=False, stop_at:bool=False, offset:VEC_2|None=None) -> VEC_2:
        p = point.copy()

        if offset:
            point += offset

        dist = (p - entity.hitbox.pos).magnitude()

        return 50 if norm > 50 else norm
    
    def react(self, entity, point:VEC_2, velocity:VEC_2|None=VEC_2(), flee:bool=False, stop_at:bool=False) -> VEC_2:
        dist = (point - entity.hitbox.pos).magnitude()
        if velocity:
            # aproximate time to catch_up
            aprox_time = dist / entity.max_speed
            inbetween_displacement = velocity * aprox_time
            point += inbetween_displacement

        wanted_velocity = (p - entity.hitbox.pos).normalize()

        if flee:
            wanted_velocity *= -1
        elif stop_at:
            if dist < self.slowing_distance:
                wanted_velocity *= dist / self.slowing_distance

        return wanted_velocity
    
    def wander_1(self, ent) -> VEC_2:
        if ent.vel.magnitude() == 0:
            ent.vel = VEC_2(0.1, 0)
        angle_max_jump = 0.1

        ent.wander_angle += random.uniform(-angle_max_jump, angle_max_jump)

        unit_vel = ent.vel.normalize()

        r = unit_vel.rotate_rad(ent.wander_angle) * ent.max_speed / 2
        a = (ent.vel.magnitude() - ent.max_speed / 2) * unit_vel

        f = r - a

        return f.normalize()
    
    def grav_center(self, ent, ent_list:list, activation_function) -> VEC_2|None:
        want = VEC_2()
        pos = ent.hitbox.pos
        max_want = 10

        for entity, dist in ent_list:
            vect = entity.hitbox.pos - pos
            want += vect * activation_function(dist)

        if want.magnitude() != 0:
            if want.magnitude() < max_want:
                return want
            else:
                return want.normalize() * max_want
        else:
            return None
        
    def align(self, ent, ent_list:list, activation_function) -> VEC_2|None:
        return None
        



class Sight:
    '''what an entity can see, maybe ray-tracing'''
    pi = math.pi

    def __init__(self, entity, precision = 32, sight_dist = 5000) -> None:
        self.entity = entity
        self.entity_manager = entity.entitie_manager
        self.point = self.entity.hitbox.pos
        self.precision = precision
        self.sight_dist = sight_dist


    def entities_in_range(self) -> list[tuple]:
        ents_in_range: list[tuple] = []
        max_region_dist = (self.sight_dist // self.entity.entity_manager.region_size) + 1
        for i in range(-max_region_dist, max_region_dist + 1):
            for j in range(-max_region_dist, max_region_dist + 1):
                region = (self.entity.region[0] + i, self.entity.region[1] + j)
                if region in self.entity_manager.regions:
                    for ent in self.entity_manager.regions[region]:
                        if ent != self.entity:
                            dist = (ent.hitbox.pos - self.point).magnitude() - ent.size / 2
                            if dist <= self.sight_dist:
                                ents_in_range.append((ent, dist))

        return ents_in_range
    
    def ents_seen(self, want_angles:bool=False) -> list|tuple[list, list]:
        ents_in_range = self.entities_in_range()
        ents_seen: list[tuple] = []
        def f(x):
            return x[1]
        ents_in_range.sort(key = f)
        angular_range_handeler = AngularRangeHandeler()
        for ent, dist in ents_in_range:
            angular_range = self.get_range(self.point, ent)
            if not angular_range_handeler.covers(angular_range):
                if ent.opaque:
                    angular_range_handeler.add(angular_range)
                # ents_seen.append((ent, dist))
            '''for testing'''
            ents_seen.append((ent, dist))

        ranges = angular_range_handeler.ranges_list
        del angular_range_handeler
        if want_angles:
            return ents_seen, ranges
        return ents_seen
    
    def get_range(self, point:VEC_2, ent) -> tuple[float, float]:
        '''eats the angular range that an entity covers for a certain point'''
        if ent.hitbox.kind == 'rect':
            if angular_range := self.get_rect_range(point, ent.hitbox):
                return angular_range
            return(0, 2 * self.pi)

        elif ent.hitbox.kind == 'circle':
            if angular_range := self.get_circle_range(point, ent.hitbox):
                return angular_range
            return(0, 2 * self.pi)
        
        raise ValueError('unknown hitbox type')
    
    def get_rect_range(self, point:VEC_2, rect) -> tuple[float, float] | None:
        '''eats the angular range that a rectangle covers for a certain point'''
        rect_corners = self.entity.entity_manager.collision_detector.rect_corners(rect)
        rel_angles = []
        rect_center: VEC_2 = rect.pos

        for corner in rect_corners:
            rel_angle = -(rect_center - point).angle_to(VEC_2(corner) - point) * PI / 180
            if abs(rel_angle) > PI:
                if rel_angle > 0:
                    rel_angle -= 2 * PI
                else:
                    rel_angle += 2 * PI
            rel_angles.append((rel_angle, corner))

        def f(x):
            return x[0]
        rel_start_angle, start_point = min(rel_angles, key = f)
        rel_end_angle, end_point = max(rel_angles, key = f)

        if False:  # Check if the center of the ent is inside the other
            # because all hitboxes are convex it means that the point is in the hitbox
            return None
        
        angles = (-VEC_2(1, 0).angle_to(VEC_2(start_point) - point) * PI / 180,
                 -VEC_2(1, 0).angle_to(VEC_2(end_point) - point) * PI / 180)
    
        return angles
    
    def get_circle_range(self, point:VEC_2, circle) -> tuple[float, float] | None:
        '''eats the angular range that a circle covers for a certain point'''
        dist = (point - circle.pos).magnitude()
        if dist <= circle.r:
            return None
        beta = abs(math.asin(circle.r / dist))
        mid_angle = -VEC_2(1, 0).angle_to(circle.pos - point) * PI / 180
        return (mid_angle - beta, mid_angle + beta)


class AngularRangeHandeler:
    '''used for the Sight
    all angles must be in rads'''
    pi = math.pi

    def __init__(self, ranges_list: list[tuple[float, float]] = []) -> None:
        self.ranges_list = ranges_list

    def clear(self) -> None:
        self.ranges_list = []

    def sort(self) -> None:
        def key_function(x):
            return x[0]
        self.ranges_list.sort(key = key_function)

    def are_equal(self, ranges_list_1, ranges_list_2) -> bool:
        '''checkes if two range lists are equal'''
        ranges_list_1 = self.remove_null_ranges(ranges_list_1)
        ranges_list_2 = self.remove_null_ranges(ranges_list_2)
        for angular_range in ranges_list_2:
            if angular_range not in ranges_list_1:
                return False
        for angular_range in ranges_list_1:
            if angular_range not in ranges_list_2:
                return False
        return True

    def remove_null_ranges(self, ranges_list) -> list[tuple[float, float]]:
        new_ranges_list = []
        for range_ in ranges_list:
            if range_[0] != range_[1]:
                new_ranges_list.append(range_)
        return  new_ranges_list

    def corect_boundries(self, angular_range:tuple[float, float]) -> tuple[float, float]:
        '''checks if boundries are false,
        for example: if the range does more than
        a full rotation or if the end crossed the zero point'''
        start, end = angular_range
        
        if start == 2 * self.pi and end == 0:  # equivilent to null range
            return (0, 0)

        # if range more than entire circle
        if abs(end - start) >= 2 * self.pi:
            start, end = 0, 2 * self.pi

        # if start not between 0 and 2*pi it corrects
        start_redundance = start // (2 * self.pi)
        end_redundance = end // (2 * self.pi)
        start -= start_redundance * 2 * self.pi
        end -= end_redundance * 2 * self.pi

        return (start, end)
        
    def combined_ranges(self, angular_range_1:tuple[float, float], angular_range_2:tuple[float, float]) -> tuple[float, float] | None:
        start_1, end_1 = self.corect_boundries(angular_range_1)
        start_2, end_2 = self.corect_boundries(angular_range_2)

        
        # check to see if they wrap arrount zero
        cross_1 = True if start_1 > end_1 else False
        cross_2 = True if start_2 > end_2 else False

        if cross_1 and cross_2:
            # they both cross zero so no need to check for a hole

            if start_1 <= start_2:

                if end_2 <= end_1:
                    return self.corect_boundries((start_1, end_1))
                if end_2 < start_1:
                    return self.corect_boundries((start_1, end_2))
                return (0, 2 * self.pi)
                
            # start_1 > start_2
            if end_1 <= end_2:
                return self.corect_boundries((start_2, end_2))
            if end_1 < start_2:
                return self.corect_boundries((start_2, end_1))
            return (0, 2 * self.pi)

        elif cross_1:
            if end_1 >= start_2:
                if end_2 >= start_1:
                    return (0, 2 * self.pi)
                if end_1 >= end_2:
                    return self.corect_boundries((start_1, end_1))
                return self.corect_boundries((start_1, end_2))
            if end_2 >= start_1:
                if start_1 <= start_2:
                    return self.corect_boundries((start_1, end_1))
                return self.corect_boundries((start_2, end_1))
            # hole
            return None
        
        elif cross_2:
            if end_2 >= start_1:
                if end_1 >= start_2:
                    return (0, 2 * self.pi)
                if end_2 >= end_1:
                    return self.corect_boundries((start_2, end_2))
                return self.corect_boundries((start_2, end_1))
            if end_1 >= start_2:
                if start_2 <= start_1:
                    return self.corect_boundries((start_2, end_2))
                return self.corect_boundries((start_1, end_2))
            # hole
            return None
        else:
            if start_1 <= start_2:
                if start_2 > end_1:
                    # there is a hole
                    return None
                if end_2 >= end_1:
                    return self.corect_boundries((start_1, end_2))
                else:
                    return self.corect_boundries((start_1, end_1))
            if start_1 > end_2:
                # there is a hole
                return None
            if end_1 >= end_2:
                return self.corect_boundries((start_2, end_1))
            else:
                return self.corect_boundries((start_2, end_2))

    def add(self, new_angular_range:tuple[float, float]) -> None:
        '''adds a range to the ranges_list without redundant overlap'''
        new_ranges_list: list[tuple[float, float]] = []
        for ang_range in self.ranges_list:
            if combined_range := self.combined_ranges(ang_range, new_angular_range):
                new_angular_range = self.corect_boundries(combined_range)
            else:
                new_ranges_list.append(self.corect_boundries(ang_range))
        new_ranges_list.append(self.corect_boundries(new_angular_range))
        self.ranges_list = new_ranges_list

    def sub(self, new_angular_range:tuple[float, float]) -> None:
        '''removes a range to the ranges_list without redundant overlap'''
        self.invert()        
        self.add(new_angular_range)
        self.invert()

    def invert(self) -> None:
        '''
        inverts the ranges_list:
        what was in the ranges is now out and what was out is now in
        '''
        temp = self.remove_null_ranges(self.ranges_list)
        self.ranges_list = temp
        self.sort()
        new_ranges_list: list[tuple[float, float]] = []
        nbr_of_ranges = len(self.ranges_list)
        if nbr_of_ranges != 0:
            for i in range(nbr_of_ranges):
                this_one = i
                nextone = i + 1 if i < nbr_of_ranges - 1 else 0
                new_range = (self.ranges_list[this_one][1], self.ranges_list[nextone][0])
                new_ranges_list.append(self.corect_boundries(new_range))
        else:
            new_ranges_list = [(0, 2 * self.pi)]
        self.ranges_list = self.remove_null_ranges(new_ranges_list)

    def fits(self, angular_range:tuple[float, float]) -> bool:
        '''checkes if a range could fit in the ranges_list without overlap'''
        original_list = self.ranges_list
        self.sub(angular_range)
        if self.are_equal(original_list, self.ranges_list):
            return True
        self.ranges_list = original_list
        return False
        
    def covers(self, angular_range:tuple[float, float]) -> bool:
        '''checkes if a range would be compleatly covered by the ranges in the list'''
        state = False
        self.invert()
        if self.fits(angular_range):
            state = True
        self.invert()
        return state
    
    def borders(self, angle:float) -> tuple[float, float]|None:
        '''returns, if the angle is in an angular range, the bounding rangles of that range'''
        if len(self.ranges_list) == 0:
            return None
        if len(self.ranges_list) == 1 and self.ranges_list[0] == (0, 2 * self.pi):
            return None
        
        redundance = angle // (2 * self.pi)
        angle -= redundance * 2 * self.pi

        for angular_range in self.ranges_list:
            if angular_range[0] < angular_range[1]:  # crosses or not
                if angular_range[0] < angle < angular_range[1]:
                    return angular_range
                break
            if angular_range[0] < angle  and angular_range[1] < angle:
                return angular_range
            if angular_range[0] > angle  and angular_range[1] > angle:
                return angular_range
            break
        return None
                

class Geometries:
    '''diffrent vector geometries'''

    def __init__(self, direction_count) -> None:
        self.direction_count = direction_count

    def do_funcion(self, angle_offset, function) -> list[float]:
        '''angle_offset needs to be in rads'''
        directions: list[float] = []
        for i in range(self.direction_count):
            angle = (i / self.direction_count) * 2 * math.pi + angle_offset
            directions.append(function(angle))
        return directions

    def f1(self, angle) -> float:
        '''angle needs to be in rads'''
        return abs(math.cos(angle))
    
    def f2(self, angle) -> float:
        '''angle needs to be in rads'''
        return math.cos(angle)
    
    def f3(self, angle) -> float:
        return math.cos(angle / 2 + math.pi / 4) ** 4


class ActivationFunctions:
    '''
    to be used on the vector geometries
    for example: when close important but when far less important
    '''
    def __init__(self) -> None:
        pass

    def f1(self, x) -> float:
        return 1/(x**4)
    
    def f2(self, x) -> float:
        return 0.345
    
    def f3(self, x) -> float:
        return 1


class Averages:
    '''diffrent type of avreges'''
    def __init__(self) -> None:
        pass

    def average_vector(self, power:float, vec_list:list[VEC_2], wheight_list:list[float] | None = None) -> VEC_2|None:
        l_x = [vec.x for vec in vec_list]
        l_y = [vec.y for vec in vec_list]
    
        average_x = self.lehmer_mean(l_x, power, wheight_list)
        average_y = self.lehmer_mean(l_y, power, wheight_list)
        if average_x != None and average_y != None:
            return VEC_2(average_x, average_y)
        return None

    def lehmer_mean(self, values:list[float], power: float, weights:list[float] | None = None) -> float|None:
        '''the if statements are for allowing negative values'''
        if not values:
            return None
        
        if weights:
            values_size = len(values)
            weights_size = len(weights)
            if values_size != weights_size:
                raise ValueError('diffrent number of values and weights')
            
        sum_1 = 0
        sum_2 = 0
        if weights:
            for i in range(values_size):
                value = values[i]
                if value == 0 and power < 1:
                    value += 0.0000000000000000001
                sum_1 += weights[i] * value ** power if value >= 0 else -weights[i] * abs(values[i]) ** power
                sum_2 += abs(weights[i]) * abs(value) ** (power - 1)
        else:
            for value_ in values:
                value = value_
                if value == 0 and power <= 0:
                    value += 0.000001
                sum_1 += value ** power if value >= 0 else -1 * abs(value) ** power
                sum_2 += abs(value) ** (power - 1)
        if sum_2 == 0:
            if sum_1 == 0:
                return 0
            raise ValueError('average not possible')
        return sum_1 / sum_2 
    
    def geo_mean(sefl, values:list[float], weights:list[float] | None = None):

        if weights:
            values_size = len(values)
            weights_size = len(weights)
            if values_size != weights_size:
                raise ValueError('diffrent number of values and weights')
            
        prod: float = 1
        n:float = 0
        if weights:
            for i in range(values_size):
                if values[i] < 0:
                    raise ValueError('negatif value')
                prod = prod * values[i] ** weights[i]
                n += weights[i]
        else:
            for value in values:
                if value < 0:
                    raise ValueError('negatif value')
                prod = prod * value
                n += 1
        return prod ** (1 / n)

    def power_mean(self, values:list[float], power: float, weights:list[float] | None = None) -> float|None:
        '''all values must be positif'''
        if not values:
            return None
        
        if power == 0:
            return self.geo_mean(values, weights)
        
        if weights:
            values_size = len(values)
            weights_size = len(weights)
            if values_size != weights_size:
                raise ValueError('diffrent number of values and weights')
            
        n: float = 0
        sum: float = 0
        if weights:
            for i in range(values_size):
                if values[i] < 0:
                    raise ValueError('negatif value')
                sum += weights[i] * values[i] ** power
                n += abs(weights[i])
        else:
            for value in values:
                if value < 0:
                    raise ValueError('negatif value')
                sum += value ** power
                n += 1
        sum = sum / n
        return sum ** (1 / power)