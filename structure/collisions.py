'''collision detection'''
import math
from settings import (
    VEC_2
)


class CollisionDetector:
    '''responsible for detecting collisions and calculating their pushout'''
    def __init__(self) -> None:
        pass

    def ent_ent_collision(self, hitbox1, hitbox2) -> VEC_2 | None:
        '''sorts which collision detection to use'''
        if hitbox1.kind == 'rect':

            if hitbox2.kind == 'rect':
                return self.rect_rect(hitbox1, hitbox2)

            elif hitbox2.kind == 'circle':
                return self.rect_circle(hitbox1, hitbox2)

        elif hitbox1.kind == 'circle':

            if hitbox2.kind == 'rect':
                return self.circle_rect(hitbox1, hitbox2)

            elif hitbox2.kind == 'circle':
                return self.circle_circle(hitbox1, hitbox2)
                
        raise ValueError('unknown hitbox type')
    
    def line_ent_collision(self, line:dict, hitbox) -> list[tuple]:
        '''sorts which collision detection to use'''
        if hitbox.kind == 'rect':
            pass
        elif hitbox.kind == 'circle':
            pass
        raise ValueError('unknown hitbox type')
    
    def line_circle_inter(self, line:dict, circle) -> list[tuple]:
        '''https://chatgpt.com/c/974e0607-9653-4e22-a183-97e730457388'''

        # Line parameters
        x0, y0 = line['start_pos']
        dx, dy = line['direction']
        l = line['length']
        
        # Circle parameters
        cx, cy = circle.pos
        r = circle.r
        
        # Coefficients of the quadratic equation at^2 + bt + c = 0
        a = dx**2 + dy**2
        b = 2 * (dx * (x0 - cx) + dy * (y0 - cy))
        c = (x0 - cx)**2 + (y0 - cy)**2 - r**2
        
        # Calculate discriminant
        discriminant = b**2 - 4 * a * c
        
        # No real solutions if discriminant is negative
        if discriminant < 0:
            return []
        
        # Calculate the two solutions for t
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (-b + sqrt_discriminant) / (2 * a)
        t2 = (-b - sqrt_discriminant) / (2 * a)
        
        # Check if the solutions are within the valid range [0, L]
        intersections: list[tuple] = []
        if 0 <= t1 <= l:
            intersections.append((x0 + t1 * dx, y0 + t1 * dy))
        if 0 <= t2 <= l:
            intersections.append((x0 + t2 * dx, y0 + t2 * dy))
        
        return intersections

    def rotate_point(self, px:float, py:float, angle:float) -> tuple[float, float]:
        """
        Rotate a point (px, py) around a referance by an angle (in radians).
        https://chatgpt.com/c/974e0607-9653-4e22-a183-97e730457388
        """

        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        x_new = px * cos_theta - py * sin_theta
        y_new = px * sin_theta + py * cos_theta
        return x_new, y_new

    def line_rect_inter(self, line:dict, rectangle) -> list[tuple[float, float]]:
        '''
        gives the intersection points between a line and a rectangle
        https://chatgpt.com/c/974e0607-9653-4e22-a183-97e730457388
        '''
        
        # Line parameters
        x0, y0 = line['start']
        dx, dy = line['direction']
        l = line['length']
        
        # Rectangle parameters
        cx, cy = rectangle.pos
        w = rectangle.width
        h = rectangle.height
        theta = rectangle.angle
        
        # Translate line to rectangle's local coordinate system
        x0_local, y0_local = x0 - cx, y0 - cy
        
        # Rotate line by -theta to align with axis-aligned rectangle
        x0_rot, y0_rot = self.rotate_point(x0_local, y0_local, -theta)
        dx_rot, dy_rot = self.rotate_point(dx, dy, -theta)
        
        # Parametric representation of the rotated line
        intersections = []
        for edge in [(-w/2, -h/2, w/2, -h/2), (-w/2, h/2, w/2, h/2), (-w/2, -h/2, -w/2, h/2), (w/2, -h/2, w/2, h/2)]:
            x1, y1, x2, y2 = edge
            denom = (x2 - x1) * dy_rot - (y2 - y1) * dx_rot
            if denom == 0:
                continue  # Lines are parallel
            t = ((x0_rot - x1) * (y2 - y1) - (y0_rot - y1) * (x2 - x1)) / denom
            if 0 <= t <= l:
                u = ((x0_rot - x1) * dy_rot - (y0_rot - y1) * dx_rot) / denom
                if 0 <= u <= 1:
                    intersection_x = x0_rot + t * dx_rot
                    intersection_y = y0_rot + t * dy_rot
                    intersections.append((intersection_x, intersection_y))
            
        # Transform intersections back to the original coordinate system
        intersections_world = [self.rotate_point(ix, iy, theta) for ix, iy in intersections]
        intersections_world = [(ix + cx, iy + cy) for ix, iy in intersections_world]
        
        return intersections_world

    def circle_circle(self, circle1, circle2) -> VEC_2 | None:
        '''circle-circle collision'''
        dist = VEC_2(circle1.pos).distance_to(VEC_2(circle2.pos))
        overlap = -(dist - circle1.r - circle2.r)
        displacement = overlap * (circle1.pos - circle2.pos).normalize()
        if dist < circle1.r + circle2.r:
            return displacement
        return None

    def smallest_vector(self, vec_list: list[VEC_2]) -> VEC_2:
        '''returns the vector with the smallest magnitude'''
        mag_list = [i.magnitude() for i in vec_list]
        smalest_mag = min(mag_list)
        index = mag_list.index(smalest_mag)
        return vec_list[index]

    def v1_same_direction_as_v2(self, v1: VEC_2, v2: VEC_2) -> VEC_2:
        '''
        returns a projection of v1 on v2 that is pointing in the same direction as v2
        similar to projection_vect
        '''
        if v2.magnitude() != 0:
            return abs(v1.dot(v2)) / v2.magnitude() * v2.normalize()
        return v1

    def rect_corners(self, rect) -> tuple[VEC_2, VEC_2, VEC_2, VEC_2]:
        '''returns the coordinates of the corners of a rect'''
        return (
            rect.pos + rect.vec1 + rect.vec2,
            rect.pos + rect.vec1 - rect.vec2,
            rect.pos - rect.vec1 + rect.vec2,
            rect.pos - rect.vec1 - rect.vec2
            )

    def projection_vect(self, projected_vector, axis_vector) -> VEC_2:
        '''returns a projection of v1 on v2'''
        return projected_vector.dot(axis_vector) * axis_vector / axis_vector.magnitude() ** 2

    def external_vectors(self, vector_list, axis_vector) -> list[VEC_2]:
        '''gives the two vectors projections on the axis would be the farthest apart'''
        axis_vector = axis_vector.normalize()
        vector_list = [vector.dot(axis_vector) for vector in vector_list]
        return [min(vector_list) * axis_vector, max(vector_list) * axis_vector]

    def progections_colliding_with_rect(self, projections, axis_vector) -> VEC_2 | None:
        '''checks if the line between the tow projections is tuching the rect'''
        axis_vector_mag = axis_vector.magnitude()
        if projections[0].dot(projections[1]) < 0:
            deepest_projection = self.smallest_vector(projections)
            return -self.v1_same_direction_as_v2(axis_vector, deepest_projection) - deepest_projection
        elif projections[0].magnitude() < axis_vector_mag or projections[1].magnitude() < axis_vector_mag:
            deepest_projection = self.smallest_vector(projections)
            return self.v1_same_direction_as_v2(axis_vector, deepest_projection) - deepest_projection
        else:
            return None

    def rect_rect(self, rect1, rect2) -> VEC_2 | None:
        '''
        insired by https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other
        Separating Axis Theorem (SAT)
        '''
        rect_vectors = [
            [rect2.vec1, rect2.vec2],
            [rect1.vec1, rect1.vec2]
        ]

        # rect corners
        rect1_corners = self.rect_corners(rect1)
        rect2_corners = self.rect_corners(rect2)

        # finding the corner projections on the two axies of the other rect
        projections = [
            [
                [self.projection_vect(VEC_2(corner) - VEC_2(rect2.pos), rect2.vec1) for corner in rect1_corners],  # (progections_on_rect2_axis1, axis_vector)
                [self.projection_vect(VEC_2(corner) - VEC_2(rect2.pos), rect2.vec2) for corner in rect1_corners]   # (progections_on_rect2_axis2, axis_vector)
            ],  # rect1
            [
                [self.projection_vect(VEC_2(corner) - VEC_2(rect1.pos), rect1.vec1) for corner in rect2_corners],  # (progections_on_rect1_axis1, axis_vector)
                [self.projection_vect(VEC_2(corner) - VEC_2(rect1.pos), rect1.vec2) for corner in rect2_corners]   # (progections_on_rect1_axis2, axis_vector)
            ],  # rect2
        ]

        # finding the external projections
        external_projections = [
            [
                self.external_vectors(projections[rect][axis], rect_vectors[rect][axis]) for axis in range(2)  # the two axies
            ] for rect in range(2)  # the two rects
        ]   # external_projections[rect][axis][the two oposite projections]

        # finding if all the lines conecting the projections hit the rectangles
        displacement_vectors = []
        for rect in range(2):
            for axis in range(2):
                if pushout := self.progections_colliding_with_rect(external_projections[rect][axis], rect_vectors[rect][axis]):
                    displacement_vectors.append(pushout if rect == 0 else -pushout)
                else:
                    return None
        return self.smallest_vector(displacement_vectors)

    def circle_rect(self, circle, rect) -> VEC_2 | None:
        '''inverses the order of the entities so that they are pushed appart instead of pulled together'''
        if pushout := self.rect_circle(rect, circle):
            return -pushout
        return None

    def rect_circle(self, rect, circle) -> VEC_2 | None:
        '''collisions between rect and circle'''
        vec1_mag = rect.vec1.magnitude()
        vec2_mag = rect.vec2.magnitude()

        distance_vector = VEC_2(rect.pos) - VEC_2(circle.pos)

        # distances to the centers of the rect along its axies
        dist_to_center_1 = distance_vector.dot(rect.vec1) / vec1_mag
        dist_to_center_2 = distance_vector.dot(rect.vec2) / vec2_mag

        abs_dist_to_center_1 = abs(dist_to_center_1)
        abs_dist_to_center_2 = abs(dist_to_center_2)

        dist_1_sign = dist_to_center_1 / abs(dist_to_center_1) if dist_to_center_1 != 0 else 1
        dist_2_sign = dist_to_center_2 / abs(dist_to_center_2) if dist_to_center_2 != 0 else 1

        # definitely not colliding
        if abs_dist_to_center_1 > vec1_mag + circle.r:
            return None
        if abs_dist_to_center_2 > vec2_mag + circle.r:
            return None

        # definitly colliding
        if abs_dist_to_center_1 <= vec1_mag:
            pushout = -rect.vec2.normalize() * (abs_dist_to_center_2 - vec2_mag - circle.r) * dist_2_sign
            return pushout
        if abs_dist_to_center_2 <= vec2_mag:
            pushout = -rect.vec1.normalize() * (abs_dist_to_center_1 - vec1_mag - circle.r) * dist_1_sign
            return pushout

        # corner cases
        d1 = abs_dist_to_center_1 - vec1_mag
        d2 = abs_dist_to_center_2 - vec2_mag
        if d1*d1 + d2*d2 <= circle.r * circle.r:
            norm = circle.r / math.sqrt(d1*d1 + d2*d2) - 1
            direction = VEC_2(-d1 * dist_1_sign, d2 * dist_2_sign)
            pushout = norm * direction
            return -pushout
        return None
