import pygame
import math

from settings import(
    VEC_2
)


class Hitbox:
    '''base hotbox class'''
    kind = 'None'

    def __init__(self, pos: tuple[float | int, float | int] | VEC_2) -> None:
        self.pos:VEC_2 = VEC_2(pos)
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
        self.size = math.sqrt(length  * length + breadth * breadth)
        self.angle = angle
        self.length, self.breadth = length, breadth
        self.vec1 = VEC_2(math.cos(angle), math.sin(angle)) * length
        self.vec2 = VEC_2(math.sin(angle), -math.cos(angle)) * breadth

    def copy(self):
        return Rectangle(self.pos, self.angle, self.length, self.breadth)

    def scale(self, scalar) -> None:
        self.vec1 = self.vec1 * scalar
        self.vec2 = self.vec2 * scalar

    def rotate(self, angle) -> None:
        self.angle += angle
        self.vec1 = self.vec1.rotate(angle)
        self.vec2 = self.vec2.rotate(angle)

    def draw(self, display_surface, camera) -> None:
        '''draws the boundries of the hitbox'''
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos + self.vec1 + self.vec2, camera.player_displacement + self.pos + self.vec1 - self.vec2, width=1)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos - self.vec1 + self.vec2, camera.player_displacement + self.pos - self.vec1 - self.vec2, width=1)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos + self.vec2 + self.vec1, camera.player_displacement + self.pos + self.vec2 - self.vec1, width=1)
        pygame.draw.line(display_surface, self.color, camera.player_displacement + self.pos - self.vec2 + self.vec1, camera.player_displacement + self.pos - self.vec2 - self.vec1, width=1)


class Circle(Hitbox):
    '''circular hitbox class'''
    kind = 'circle'

    def __init__(self, center, radius) -> None:
        super().__init__(center)
        self.r = radius
        self.size = 2 * radius

    def copy(self):
        return Circle(self.pos, self.r)

    def scale(self, scalar) -> None:
        self.r = self.r * scalar

    def draw(self, display_surface, camera) -> None:
        '''draws the boundries of the hitbox'''
        pygame.draw.circle(display_surface, self.color, camera.player_displacement + self.pos, self.r, 1)

    

class DrawAngle:

    def __init__(self, point, ranges_list):
        self.point = point
        self.ranges_list = ranges_list

    def draw_one(self, display_surface, camera, point, start, end):
        dist = 100
        v1 = VEC_2(100, 0).rotate_rad(-start)
        v2 = VEC_2(100, 0).rotate_rad(-end)
        pos = point + camera.player_displacement
        rect = pygame.rect.Rect(pos - VEC_2(dist, dist),  (dist * 2, dist * 2))
        pygame.draw.arc(display_surface, 'blue', rect, start, end, 5)
        pygame.draw.line(display_surface, 'blue', pos, pos + v1)
        pygame.draw.line(display_surface, 'blue', pos, pos + v2)

    def draw(self, display_surface, camera):
        for start, end in self.ranges_list:
            self.draw_one(display_surface, camera, self.point, -end, -start)

class DrawPoints:

    def __init__(self):
        self.point_list = []

    def add_point(self, pos):
        self.point_list.append(pos)

    def clear(self):
        self.point_list = []

    def draw(self, display_surface, camera):
        for point in self.point_list:
            pygame.draw.circle(display_surface, 'red', point + camera.player_displacement, 5)

class Line:
    def __init__(self):
        self.list:list = []
        
    def add(self, start:VEC_2, end:VEC_2, color:str, width:int = 3):
        self.list.append((start, end, color, width))

    def clear(self):
        self.list:list = []

    def draw(self, display_surface, camera):
        for line in self.list:
            pygame.draw.line(display_surface, line[2], line[0] + camera.player_displacement, line[1] + camera.player_displacement, line[3])

