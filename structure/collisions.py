import pygame, sys, time
from settings import(
    VEC_2
)

class Collision_detector:
    def __init__(self):
        pass

    def circle_circle(self, pos1, r1, pos2, r2):
        dist = VEC_2(pos1).distance_to(VEC_2(pos2))
        if dist < r1 + r2: return True
        return False
    
    def Rect_Circle(self, circle, rect):  # cilrcle = {'pos': tuple, 'r': int}, rect = {'pos': tuple, 'vec1':vect, 'vec2':vect} vec1, vec2 perpendicular
        vec1_mag = rect['vec1'].magnitude()
        vec2_mag = rect['vec2'].magnitude()
        if rect['vec1'].dot(rect['vec2']) != 0:
            raise ValueError("The vectors aren't perpendicular.")
        if vec1_mag == 0 or vec2_mag == 0:
            raise ValueError("A vector in null.")
        
        
        distance_vector = VEC_2(rect['pos']) - VEC_2(circle['pos'])

        dist_to_center_1 = abs(distance_vector.dot(rect['vec1'])) / vec1_mag # distance to the rect center anolg the axis 1
        dist_to_center_2 = abs(distance_vector.dot(rect['vec1'])) / vec2_mag # distance to the rect center anolg the axis 2

        # definitely not colliding
        if (dist_to_center_1 > vec1_mag + circle['r']): return False
        if (dist_to_center_2 > vec2_mag + circle['r']): return False
        # definitly colliding
        if (dist_to_center_1 <= vec1_mag): return True 
        if (dist_to_center_2 <= vec2_mag): return True
        # corner cases
        d1 = dist_to_center_1 - vec1_mag
        d2 = dist_to_center_1 - vec2_mag
        return (d1*d1 + d2*d2 <= circle['r']*circle['r'])