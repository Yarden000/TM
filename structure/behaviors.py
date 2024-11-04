
import random
import math
import numpy
from typing import Any
from math import pi
from settings import (
    PY_VEC_2,
    angle_between_vectors_0_to_2pi,
    angle_between_vectors_plus_minus_pi
)
from visualizing import(
    Line
)


visuals = []


class Behavior:
    '''where all the behavior calculations are done'''
    def __init__(self, entity_manager, ent) -> None:
        self.entity_manager = entity_manager
        self.entity = ent
        self.StateCalc = StateCalc(ent)
        self.collision_avoidance_handler = CollisionAvoidanceHandler()
        self.Sight = Sight(ent)
        self.InterestCalc = InterestCalc(ent)



    def wants(self) -> tuple:
        '''gives the things an entity wants to do, (a direction to move in, and an action to do)'''
        ents_seen: list = self.Sight.ents_seen()
        amount, objectif_ent = self.InterestCalc.interest(ents_seen, 'food')
        if objectif_ent:
            direction = self.direction_after_col(objectif_ent, ents_seen)
            # not jet implemented
            action = None
            return (direction, action)
        return (PY_VEC_2(0, 0), None)
        # raise ValueError('not implemented')

    def direction_after_col(self, objectif_ent, ents_seen):
        '''whitch direction is suposed to go to avoid collision and go towards objective'''
        reaction_dist: float = 200  # distance of collision avoidance (if further inored)
        direction: PY_VEC_2 = self.collision_avoidance_handler.avoid_collision(self.entity, objectif_ent, ents_seen, reaction_dist)
        return direction


    
class CollisionAvoidanceHandler:

    def __init__(self) -> None:
        self.angular_range_handeler = AngularRangeHandeler()

    def circle_circle(self, circle_1, circle_2) -> tuple[float, float]|None:
        '''returns the minimum and maximum angles to
        avoid a collision between two circles'''

        dist = (circle_1.body.position - circle_2.body.position).length
        temp = (circle_1.radius + circle_2.radius) / dist
        angle = -(circle_2.body.position - circle_1.body.position).get_angle_between(PY_VEC_2(1, 0))

        if temp > 1:
            beta = pi * 2 / 3
            return (angle - beta, angle + beta)

        alpha = math.asin(temp)
        return (angle - alpha, angle + alpha)
    
    def circle_rect(self, circle, rect, invert:bool=False) -> tuple[float, float]|None:
        '''returns the minimum and maximum angles to
        avoid a collision between a circle and a rect'''

        dist = (circle.body.position - rect.body.position).length

        raise ValueError('not implemented')

    def rect_rect(self, rect_1, rect_2) -> tuple[float, float]|None:
        '''returns the minimum and maximum angles to
        avoid a collision between two rects'''

        dist = (rect_1.body.position - rect_2.body.position).length

        raise ValueError('not implemented')
    
    def avoid_collision(self, ent, ent_want, ent_list:list, distance:float|None=1000) -> PY_VEC_2:  # distance should be in proportion to the speed
        '''returns the minimum and maximum angles to
        avoid a collision'''
        self.angular_range_handeler.clear()
        ent_self_hitbox = ent.shape
        direction_to_ent_want = ent_want.body.position - ent.body.position
        distance_to_ent_want = direction_to_ent_want.length


        # for removing the objectif
        def in_tuple_list(list, x):
            for tuple_ in list:
                if x in tuple_:
                    return tuple_
            return False
        if temp := in_tuple_list(ent_list, ent_want):
            ent_list.remove(temp)

        for entity, dist in ent_list:
            if dist.length <= distance and dist.length <= distance_to_ent_want:
                ent_other_hitbox = entity.shape
                if ent.hitbox_shape == 'circle':

                    if ent.hitbox_shape == 'circle':

                        if ang_range := self.circle_circle(ent_self_hitbox, ent_other_hitbox):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return PY_VEC_2(0, 0)
                        
                    else:

                        if ang_range := self.circle_rect(ent_self_hitbox, ent_other_hitbox):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return PY_VEC_2(0, 0)
                        
                else:

                    if ent_other_hitbox.kind == 'circle':

                        if ang_range := self.circle_rect(ent_other_hitbox, ent_self_hitbox, invert = True):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return PY_VEC_2(0, 0)
                        
                    else:

                        if ang_range := self.rect_rect(ent_self_hitbox, ent_other_hitbox):
                            self.angular_range_handeler.add(ang_range)
                        else:
                            return PY_VEC_2(0, 0)
                    
        #ent.other_hitboxes['seeing_angle'] = DrawAngle(ent.hitbox.pos, self.angular_range_handeler.ranges_list)
        
        angle = direction_to_ent_want.angle
        if angles := self.angular_range_handeler.borders(angle):
            #print(angles)
            v1 = PY_VEC_2(1, 0).rotated(angles[0])
            v2 = PY_VEC_2(1, 0).rotated(angles[1])
            def f(x:PY_VEC_2):
                return x.dot(direction_to_ent_want.normalized())
            best_direction = max([v1, v2], key = f)
            
            # print('react')
            return best_direction
        # print('ignore')
        
        return direction_to_ent_want.normalized()


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
   

class StateCalc:
    '''calculates whitch interest is most important and changes the state of the animal'''
    def __init__(self, ent):
        self.ent = ent
        self.current_state = None
        self.state_importance_threashold = 10  # needs to be in genome
        self.states = {
            'food': (None, None),
            'danger': (None, None),
            # 'mating': (None, None)
        }

    def next_state(self):
        raise ValueError('not implemented')

    def update_states(self):
        raise ValueError('not implemented')
    

class Sight:
    '''what an entity can see, maybe ray-tracing'''

    def __init__(self, entity, sight_dist = 5000) -> None:
        self.entity = entity
        self.entity_manager = entity.entity_manager
        self.point = self.entity.body.position
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
                            dist_vec = ent.body.position - self.point
                            dist = dist_vec.length - ent.size / 2
                            if dist <= self.sight_dist:
                                ents_in_range.append((ent, dist_vec))

        return ents_in_range
    
    def ents_seen(self, want_angles:bool=False) -> list|tuple[list, list]:
        '''all the ents self.ent can see'''
        ents_in_range = self.entities_in_range()
        ents_seen: list[tuple] = []
        def f(x):
            return x[1].length
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
    
    def get_range(self, point:PY_VEC_2, ent) -> tuple[float, float]:
        '''gets the angular range that an entity covers for a certain point'''
        if ent.hitbox_shape == 'rect':
            if angular_range := self.get_rect_range(point, ent.shape):
                return angular_range
            return(0, 2 * pi)

        elif ent.hitbox_shape == 'circle':
            if angular_range := self.get_circle_range(point, ent.shape):
                return angular_range
            return(0, 2 * pi)
        
        raise ValueError('unknown hitbox type')
    
    def rect_corners(self, rect):
        relative_rect_corners = rect.get_vertices()
        absolute_rect_corners = [corner + rect.body.position for corner in relative_rect_corners]
        return absolute_rect_corners
    
    def get_rect_range(self, point, rect) -> tuple[float, float] | None:
        '''eats the angular range that a rectangle covers for a certain point'''
        rect_corners = self.rect_corners(rect)
        rel_angles = []
        rect_center = rect.body.position

        for corner in rect_corners:
            rel_angle = -(rect_center - point).get_angle_between(corner - point)
            if abs(rel_angle) > pi:
                if rel_angle > 0:
                    rel_angle -= 2 * pi
                else:
                    rel_angle += 2 * pi
            rel_angles.append((rel_angle, corner))

        def f(x):
            return x[0]
        rel_start_angle, start_point = min(rel_angles, key = f)
        rel_end_angle, end_point = max(rel_angles, key = f)

        if False:  # Check if the center of the ent is inside the other
            # because all hitboxes are convex it means that the point is in the hitbox
            return None
        
        angles = (-PY_VEC_2(1, 0).get_angle_between(start_point - point),
                 -PY_VEC_2(1, 0).get_angle_between(end_point - point))
    
        return angles
    
    def get_circle_range(self, point:PY_VEC_2, circle) -> tuple[float, float] | None:
        '''eats the angular range that a circle covers for a certain point'''
        dist = (point - circle.body.position).length
        if dist <= circle.radius:
            return None
        beta = abs(math.asin(circle.radius / dist))
        mid_angle = -PY_VEC_2(1, 0).get_angle_between(circle.body.position - point)
        return (mid_angle - beta, mid_angle + beta)


class InterestCalc:
    '''in charge of claculating the amount of a certain interest,
    and the most important entity of said interest, like food, danger ...'''

    def __init__(self, ent):
        self.ent = ent  # useless
        self.WeightFuncion = WeightFunctions()
        self.Averages = Averages()

    def interest_amount(self, ent, interest_type) -> float:
        return ent.interests[interest_type]

    def weights_and_directions(self, ents_seen, weight_function, interest_type):
        weights = []
        directions = []
        for ent, direction in ents_seen:  # dist is vect
            distance = direction.length

            '''not implemented'''
            interest_amount: float = self.interest_amount(ent, interest_type)

            weights.append(weight_function(distance) * interest_amount)
            directions.append(direction.normalized())

        return weights, directions

    def vip(self, ents_seen, weights, gradient):
        '''returns the ent who is most inline with the gradient and clostest'''
        if gradient:
            radial_weight_function = lambda x: -1/360 * x + 1  # should be in genome
            l = []
            for i, ent_dist in enumerate(ents_seen):
                ent, dist = ent_dist
                theta = abs(gradient.get_angle_degrees_between(dist))
                l.append((radial_weight_function(theta) * weights[i], ent))
        else:
            l = []
            for i, ent_dist in enumerate(ents_seen):
                ent, dist = ent_dist
                l.append((weights[i], ent))
        if l:
            return max(l, key = lambda x: x[0])[1]
        return None


    def interest(self, ents_seen, interest_type:str) -> tuple[float, Any]:
        weight_function = lambda x: self.WeightFuncion.poly(x)  # p and a should be in genome

        # can be optimized
        weights, directions = self.weights_and_directions(ents_seen, weight_function, interest_type)

        amount = sum(weights)

        gradient = self.Averages.arithmetic_average_vect(directions, weights)

        # visuals
        if gradient:
            visuals.append(Line(self.ent.body.position, gradient * 100, (200, 0, 0)))

        best_ent = self.vip(ents_seen, weights, gradient)
        
        return amount, best_ent

    
class WeightFunctions:

    def __init__(self):
        pass

    def poly(self, x:float, p:float=1/2, a:float=0.1) -> float:
        if x <= 0:
            raise ValueError('x <= 0')

        return 1 / (1 + a * x ** p)
    
    def exp(self, x:float, a:float=0.01, b:float=0.001) -> float:
        if x <= 0:
            raise ValueError('x <= 0')
        
        return numpy.exp(-a * x ** b)
     


class Steering:

    def __init__(self) -> None:
        self.slowing_distance = 200

    def max_delta_v(self, norm, angle=0):  # angle is in refrence to f^direction
        '''
        is possible to add a geometry
        example https://www.red3d.com/cwr/steer/gdc99/ figure 2
        '''
        return 100 if norm > 100 else norm
        
    def leading_the_target(self, p1:PY_VEC_2, v1:PY_VEC_2, p2:PY_VEC_2, s2:float, max_trailing:float=1.0) -> PY_VEC_2:
        dist_vect = p2 - p1
        d = dist_vect.length
        s1 = v1.length
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
  
    def react(self, entity, point:PY_VEC_2, velocity:PY_VEC_2|None=None, flee:bool=False, stop_at:bool=False, offset:PY_VEC_2|None=None) -> PY_VEC_2:
        p = point.copy()

        if offset:
            point += offset

        dist = (p - entity.hitbox.pos).length
        '''
        print('dist')
        print(point)
        '''
        if velocity:
            p = self.leading_the_target(point, velocity, entity.hitbox.pos, entity.max_speed, max_trailing=2)

        wanted_velocity = (p - entity.hitbox.pos).normalized() * entity.max_speed

        if flee:
            wanted_velocity *= -1
        elif stop_at:
            if dist < self.slowing_distance:
                wanted_velocity *= dist / self.slowing_distance

        delta_v: PY_VEC_2 = wanted_velocity - entity.vel
        if delta_v.length != 0:
            delta_v = self.max_delta_v(delta_v.length) * delta_v.normalized()

        return delta_v



class Averages:
    '''diffrent type of avreges'''
    def __init__(self) -> None:
        pass

    def lehmer_average_vector(self, power:float, vec_list:list[PY_VEC_2], wheight_list:list[float] | None = None) -> PY_VEC_2|None:
        l_x = [vec.x for vec in vec_list]
        l_y = [vec.y for vec in vec_list]
    
        average_x = self.lehmer_mean(l_x, power, wheight_list)
        average_y = self.lehmer_mean(l_y, power, wheight_list)
        if average_x != None and average_y != None:
            return PY_VEC_2(average_x, average_y)
        return None
    
    def arithmetic_average_vect(self, vec_list:list[PY_VEC_2], wheight_list:list[float] | None = None) -> PY_VEC_2|None:
        if not vec_list:
            return None
        list_ = [vec * wheight_list[i] for i, vec in enumerate(vec_list)]
        total = PY_VEC_2(0, 0)
        for v in list_:
            total += v
        if sum(wheight_list) == 0:
            return None
        return total / sum(wheight_list)

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
    
