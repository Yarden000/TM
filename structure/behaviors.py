'''
inspired by: https://www.youtube.com/watch?v=6BrZryMz-ac&t=334s   25 juin


Idea:
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
    angle_between_vectors
)

class Behavior:
    '''where all the behavior calculations are done'''
    def __init__(self, entity_manager) -> None:
        self.entity_manager = entity_manager
        self.Sight = Sight()
        self.Geometries = Geometries(16)
        self.ActivationFunctions = ActivationFunctions()

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
        rel_pos = [ent.hittbox.pos - self.entity_manager.player.hittbox.pos for ent in self.entity_manager.test_ents]
        interests: dict[str, dict] = {
            'ent_type_1': {'rel_vects': [rel_pos[0]], 'geo_func': self.Geometries.f1, 'activ_func': self.ActivationFunctions.f1, 'priority': 2},
            'ent_type_2': {'rel_vects': [rel_pos[1]], 'geo_func': self.Geometries.f2, 'activ_func': self.ActivationFunctions.f2, 'priority': 4},
            'ent_type_3': {'rel_vects': [rel_pos[2]], 'geo_func': self.Geometries.f3, 'activ_func': self.ActivationFunctions.f3, 'priority': 1}
        }

        return VEC_2()
    
    def calc_comp_geo(self, interests) -> list[float]:
        total_directions: list[float] = []
        all_directions:list[tuple[list[float]]] = []
        for vect in interests['ent_type_1']['rel_vects']:
            angle, dist = angle_between_vectors(vect, VEC_2()), vect.magnitude
            directions = self.Geometries.do_funcion(angle, interests['ent_type_1']['geo_func'])
            all_directions.append((directions, dist))

        for i in range(self.Geometries.direction_count):
            direction_avrege = 
            total_directions.append()
            for directions_ in all_directions:


        return []


class Sight:
    '''what an entity can see, maybe ray-tracing'''

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
        return math.cos(angle) ** 3


class ActivationFunctions:
    '''
    to be used on the vector geometries
    for example: when close important but when far less important
    '''
    def __init__(self) -> None:
        pass

    def f1(self, x) -> float:
        return 0.8
    
    def f2(self, x) -> float:
        return 0.345
    
    def f3(self, x) -> float:
        return x * 2


class Averages:
    '''diffrent type of avreges'''
    def __init__(self) -> None:
        pass

    def lehmer_mean(self, values:list[float], power: float, weights:list[float] | None = None) -> float:
        '''all values must be positif'''
        if weights:
            values_size = len(values)
            weights_size = len(weights)
            if values_size != weights_size:
                raise ValueError('diffrent number of values and weights')
        sum_1 = 0
        sum_2 = 0
        if weights:
            for i in range(values_size):
                sum_1 += values[i] ** power * weights[i]
                sum_2 += values[i] ** (power - 1) * weights[i]
        else:
            for value in values:
                sum_1 += value ** power
                sum_2 += value ** (power - 1)
        return sum_1 / sum_2

    def power_mean(self, values:list[float], power: float, weights:list[float] | None = None) -> float:
        '''all values must be positif'''
        if weights:
            values_size = len(values)
            weights_size = len(weights)
            if values_size != weights_size:
                raise ValueError('diffrent number of values and weights')
        n = 0
        sum = 0
        if weights:
            for i in range(values_size):
                sum += values[i] ** power * weights[i]
                n += weights[i]
        else:
            for value in values:
                n += 1
                sum += value ** power
        sum = sum / n
        return sum ** (1 / power)

    def f_mean(self, values:list[float], function:function, weights:list[float] | None = None) -> float:
        '''
        function needs to be continuous and injective(have a reciprocal),
        all values must be positif
        '''
        pass