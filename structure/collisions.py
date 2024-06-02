import pygame, sys, time
from settings import(
    VEC_2
)

class Collision_detector:
    def __init__(self):
        pass

    def circle_circle(self, circle1, circle2):
        dist = VEC_2(circle1.pos).distance_to(VEC_2(circle2.pos))
        if dist < circle1.r + circle2.r: return True
        return False
    
    def rect_circle(self, circle, rect):  # cilrcle = {'pos': tuple, 'r': int}, rect = {'pos': tuple, 'vec1':vect, 'vec2':vect} vec1, vec2 perpendicular
        vec1_mag = rect.vec1.magnitude()
        vec2_mag = rect.vec2.magnitude()
        if rect.vec1.dot(rect.vec2) != 0:
            raise ValueError("The vectors aren't perpendicular.")
        if vec1_mag == 0 or vec2_mag == 0:
            raise ValueError("A vector in null.")
        
        distance_vector = VEC_2(rect.pos) - VEC_2(circle.pos)

        dist_to_center_1 = abs(distance_vector.dot(rect.vec1)) / vec1_mag # distance to the rect center anolg the axis 1
        dist_to_center_2 = abs(distance_vector.dot(rect.vec2)) / vec2_mag # distance to the rect center anolg the axis 2

        # definitely not colliding
        if (dist_to_center_1 > vec1_mag + circle.r): return False
        if (dist_to_center_2 > vec2_mag + circle.r): return False
        # definitly colliding
        if (dist_to_center_1 <= vec1_mag): return True 
        if (dist_to_center_2 <= vec2_mag): return True
        # corner cases
        d1 = dist_to_center_1 - vec1_mag
        d2 = dist_to_center_2 - vec2_mag
        return(d1*d1 + d2*d2 <= circle.r * circle.r)

    def rect_rect(self, rect1, rect2):  # insired by https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other
                #rect corners
        rect1_corners = (
            rect1.pos + rect1.vec1 + rect1.vec2, 
            rect1.pos + rect1.vec1 - rect1.vec2, 
            rect1.pos - rect1.vec1 + rect1.vec2, 
            rect1.pos - rect1.vec1 - rect1.vec2
        )
        rect2_corners = (
            rect2.pos + rect2.vec1 + rect2.vec2, 
            rect2.pos + rect2.vec1 - rect2.vec2, 
            rect2.pos - rect2.vec1 + rect2.vec2, 
            rect2.pos - rect2.vec1 - rect2.vec2
        )
        # finding the corner projections on the two axies of the other rect
        rect1_progections_on_rect2_axis1 = []
        rect1_progections_on_rect2_axis2 = []
        for corner in rect1_corners:
            distance_vector = VEC_2(corner) - VEC_2(rect2.pos) 
            rect1_progections_on_rect2_axis1.append((distance_vector.dot(rect2.vec1) * rect2.vec1) / (rect2.vec1.magnitude() ** 2))
            rect1_progections_on_rect2_axis2.append((distance_vector.dot(rect2.vec2) * rect2.vec2) / (rect2.vec2.magnitude() ** 2))

        rect2_progections_on_rect1_axis1 = []
        rect2_progections_on_rect1_axis2 = []
        for corner in rect2_corners:
            distance_vector = VEC_2(corner) - VEC_2(rect1.pos) 
            rect2_progections_on_rect1_axis1.append((distance_vector.dot(rect1.vec1) * rect1.vec1) / (rect1.vec1.magnitude() ** 2))
            rect2_progections_on_rect1_axis2.append((distance_vector.dot(rect1.vec2) * rect1.vec2) / (rect1.vec2.magnitude() ** 2))
            
        # finding the external projections
        list = [projection.dot(rect2.vec1.normalize()) for projection in rect1_progections_on_rect2_axis1]
        external_rect1_progections_on_rect2_axis1 = (min(list) * rect2.vec1.normalize(), max(list) * rect2.vec1.normalize())

        list = [projection.dot(rect2.vec2.normalize()) for projection in rect1_progections_on_rect2_axis2]
        external_rect1_progections_on_rect2_axis2 = (min(list) * rect2.vec2.normalize(), max(list) * rect2.vec2.normalize())

        list = [projection.dot(rect1.vec1.normalize()) for projection in rect2_progections_on_rect1_axis1]
        external_rect2_progections_on_rect1_axis1 = (min(list) * rect1.vec1.normalize(), max(list) * rect1.vec1.normalize())

        list = [projection.dot(rect1.vec2.normalize()) for projection in rect2_progections_on_rect1_axis2]
        external_rect2_progections_on_rect1_axis2 = (min(list) * rect1.vec2.normalize(), max(list) * rect1.vec2.normalize())

        # finding if all the lines conecting the projections hit the rectangles
        requirement1 = False
        requirement2 = False
        requirement3 = False
        requirement4 = False
        if external_rect1_progections_on_rect2_axis1[0].dot(external_rect1_progections_on_rect2_axis1[1]) < 0:
            requirement1 = True
        elif external_rect1_progections_on_rect2_axis1[0].magnitude() < rect2.vec1.magnitude() or external_rect1_progections_on_rect2_axis1[1].magnitude() < rect2.vec1.magnitude():
            requirement1 = True
        else: 
            return False 

        if external_rect1_progections_on_rect2_axis2[0].dot(external_rect1_progections_on_rect2_axis2[1]) < 0:
            requirement2 = True
        elif external_rect1_progections_on_rect2_axis2[0].magnitude() < rect2.vec2.magnitude() or external_rect1_progections_on_rect2_axis2[1].magnitude() < rect2.vec2.magnitude():
            requirement2 = True
        else: 
            return False

        if external_rect2_progections_on_rect1_axis1[0].dot(external_rect2_progections_on_rect1_axis1[1]) < 0:
            requirement3 = True
        elif external_rect2_progections_on_rect1_axis1[0].magnitude() < rect1.vec1.magnitude() or external_rect2_progections_on_rect1_axis1[1].magnitude() < rect1.vec1.magnitude():
            requirement3 = True
        else: 
            return False

        if external_rect2_progections_on_rect1_axis2[0].dot(external_rect2_progections_on_rect1_axis2[1]) < 0:
            requirement4 = True
        elif external_rect2_progections_on_rect1_axis2[0].magnitude() < rect1.vec2.magnitude() or external_rect2_progections_on_rect1_axis2[1].magnitude() < rect1.vec2.magnitude():
            requirement4 = True
        else: 
            return False

        if requirement1 and requirement2 and requirement3 and requirement4:
            return True