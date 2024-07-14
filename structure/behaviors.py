'''
inspired by: https://www.youtube.com/watch?v=6BrZryMz-ac&t=334s   25 juin


Idea: angle
    When an animal sees something it will have a an array of vector geometriesthat will be created
    in response that are combined in proportion to their weigths. It will 'chose' a direction based 
    on the resultant vector geometry. Every thing an animal can see has an array 'activation function'
    and weights, it will either combine or choose a function based on the weights and 'pass' the norm
    of the direction-vector 'throught the 'activation function' ade the result will be the 'want' of the
    animal to go in that direction. Then it will 'choose'/combine the wants based on their weights and 
    the result will be the direction the creature will go.

All weights will be passed on hereditairly with random mutations. (Evolution!!!)
'''

import math
from settings import (
    VEC_2,
    angle_between_vectors_0_to_2pi,
    angle_between_vectors_plus_minus_pi
)

class Behavior:
    '''where all the behavior calculations are done'''
    def __init__(self, entity_manager, ent) -> None:
        self.entity_manager = entity_manager
        self.entity = ent
        self.Sight = Sight(ent)
        self.Geometries = Geometries(16)
        self.ActivationFunctions = ActivationFunctions()
        self.Averages = Averages()

        '''
        # for now
        rel_pos = [ent.hitbox.pos - self.entity_manager.player.hitbox.pos for ent in self.entity_manager.test_ents]
        self.interests: dict[str, dict] = {
            'ent_type_1': {'rel_vects': [rel_pos[0], rel_pos[1], rel_pos[2]], 'geo_func': self.Geometries.f1, 'activ_func': self.ActivationFunctions.f1, 'priority': 2},
            'ent_type_2': {'rel_vects': [rel_pos[1]], 'geo_func': self.Geometries.f2, 'activ_func': self.ActivationFunctions.f2, 'priority': 4},
            'ent_type_3': {'rel_vects': [rel_pos[2]], 'geo_func': self.Geometries.f3, 'activ_func': self.ActivationFunctions.f3, 'priority': 1}
        }
        '''
    def movement(self) -> VEC_2:  # testing$
        '''
        interests = {
            'ent_type_1': [ent1, ent2, ent3, ...],
            'ent_type_2': [ent1, ent2, ent3, ...]
            .
            .
            .
        }
        '''
        rel_pos = [ent.hitbox.pos - self.entity_manager.player.hitbox.pos for ent in self.entity_manager.test_ents]
        interests: dict[str, dict] = {
            'ent_type_1': {'rel_vects': [rel_pos[0]], 'geo_func': self.Geometries.f1, 'activ_func': self.ActivationFunctions.f1, 'priority': 2},
            'ent_type_2': {'rel_vects': [rel_pos[1]], 'geo_func': self.Geometries.f2, 'activ_func': self.ActivationFunctions.f2, 'priority': 4},
            'ent_type_3': {'rel_vects': [rel_pos[2]], 'geo_func': self.Geometries.f3, 'activ_func': self.ActivationFunctions.f3, 'priority': 1}
        }

        return VEC_2()
    
    def calc_comp_geo(self) -> list[float]:
        rel_pos = [ent.hitbox.pos - self.entity_manager.player.hitbox.pos for ent in self.entity_manager.test_ents]
        self.interests: dict[str, dict] = {
            'ent_type_1': {'rel_vects':rel_pos, 'geo_func': self.Geometries.f3, 'activ_func': self.ActivationFunctions.f1, 'priority': 2},
            'ent_type_2': {'rel_vects': [], 'geo_func': self.Geometries.f2, 'activ_func': self.ActivationFunctions.f2, 'priority': 4},
            'ent_type_3': {'rel_vects': [], 'geo_func': self.Geometries.f3, 'activ_func': self.ActivationFunctions.f3, 'priority': 1}
        }

        total_directions: list[float] = []
        all_directions: list[tuple[list[float], float]] = []  # list of all direction geometires and their weights 
        for vect in self.interests['ent_type_1']['rel_vects']:
            angle, dist = -angle_between_vectors_0_to_2pi(vect, VEC_2(1, 0)), vect.magnitude()
            directions = self.Geometries.do_funcion(angle, self.interests['ent_type_1']['geo_func'])
            all_directions.append((directions, self.interests['ent_type_1']['activ_func'](dist)))

        for i in range(self.Geometries.direction_count):
            strengths = [interest[0][i] for interest in all_directions]
            weights = [interest[1] for interest in all_directions]
            direction_avrege = self.Averages.power_mean(strengths, 1, weights)
            total_directions.append(direction_avrege)
        return total_directions


class Sight:
    '''what an entity can see, maybe ray-tracing'''
    pi = math.pi

    def __init__(self, entity, precision = 32, sight_dist = 200) -> None:
        self.entity = entity
        self.point = self.entity.hitbox.pos
        self.precision = precision
        self.sight_dist = sight_dist


    def entities_in_range(self) -> list[tuple]:
        ents_in_range: list[tuple] = []
        max_region_dist = (self.sight_dist // self.entity.entity_manager.region_size) + 1
        for i in range(-max_region_dist, max_region_dist + 1):
            for j in range(-max_region_dist, max_region_dist + 1):
                region = (self.entity.region[0] + i, self.entity.region[1] + j)
                for ent in region:
                    dist = (ent.hitbox.pos - self.point).magnitude() - ent.size / 2
                    if dist <= self.sight_dist:
                        ents_in_range.append((ent, dist))

        return ents_in_range
    
    def ents_seen(self) -> list:
        ents_in_range = self.entities_in_range()
        ents_seen: list[tuple] = []
        def f(x):
            x[1]
        ents_in_range.sort(key = f)
        angular_range_handeler = AngularRangeHandeler()
        for ent, dist in ents_in_range:
            angular_range = self.get_range(self.point, ent)
            if not angular_range_handeler.covers(angular_range):
                if ent.opaque:
                    angular_range_handeler.add(angular_range)
                ents_seen.append((ent, dist))
        del angular_range_handeler
        
        return ents_seen
    
    def get_range(self, point:VEC_2, ent) -> tuple[float, float]:
        '''eats the angular range that an entity covers for a certain point'''
        if ent.hitbox == 'rect':
            if angular_range := self.get_rect_range(point, ent.hitbox):
                return angular_range
            return(0, 2 * self.pi)

        elif ent.hitbox == 'circle':
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
            rel_angle = angle_between_vectors_plus_minus_pi(rect_center - point, VEC_2(corner) - point)
            rel_angles.append((rel_angle, corner))
        def f(x):
            return x[1]
        rel_start_angle, start_point = min(rel_angles, key = f)
        rel_end_angle, end_point = max(rel_angles, key = f)
        if rel_end_angle - rel_start_angle > self.pi:
            # because all hitboxes are convex it means that the point is in the hitbox
            return None
        angles = (angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(end_point) - point),
                 angle_between_vectors_0_to_2pi(VEC_2(1, 0), VEC_2(start_point) - point))
        return angles
    
    def get_circle_range(self, point:VEC_2, circle) -> tuple[float, float] | None:
        '''eats the angular range that a circle covers for a certain point'''
        dist = (point - circle.pos).magnitude()
        if dist <= circle.r:
            return None
        beta = abs(math.asin(circle.r / dist))
        mid_angle = angle_between_vectors_0_to_2pi(VEC_2(1, 0), circle.pos - point)
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
        if end - start >= 2 * self.pi:
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
        return x * 2


class Averages:
    '''diffrent type of avreges'''
    def __init__(self) -> None:
        pass

    def lehmer_mean(self, values:list[float], power: float, weights:list[float] | None = None) -> float:
        '''the if statements are for allowing negative values'''

        if weights:
            values_size = len(values)
            weights_size = len(weights)
            if values_size != weights_size:
                raise ValueError('diffrent number of values and weights')
            
        sum_1 = 0
        sum_2 = 0
        if weights:
            for i in range(values_size):
                sum_1 += weights[i] * values[i] ** power if values[i] >= 0 or power % 2 == 1 else -weights[i] * abs(values[i]) ** power
                sum_2 += weights[i] * values[i] ** (power - 1) if values[i] >= 0 or power % 2 == 1 else weights[i] * abs(values[i]) ** power
        else:
            for value in values:
                sum_1 += value ** power if value >= 0 or power % 2 == 1 else -1 * abs(value) ** power
                sum_2 += value ** (power - 1) if value >= 0 or power % 2 == 1 else abs(value) ** power
        if sum_2 == 0:
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

    def power_mean(self, values:list[float], power: float, weights:list[float] | None = None) -> float:
        '''all values must be positif'''

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


'''
    def f_mean(self, values:list[float], function: function, weights:list[float] | None = None) -> float:
    
        A GENBERALIZES POWER MEAN:
        function needs to be continuous and injective(have a reciprocal),
        all values must be positif
    
        return 3.9
'''