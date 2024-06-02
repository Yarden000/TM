'''
this file is only used for testing and wont be used in the game
'''

import numpy as np
import pygame, sys
import random
import math
'''
a = np.empty((4, 4), '<U5')
print(a)

a[1, 1] = 'hello'
print(a)



a = np.array([pygame.image.load('../graphics/test/desert.png'), pygame.image.load('../graphics/test/plains.png')])
print(a.dtype)

a = np.empty((4, 4), 'object')
print(a)
a[1, 1] = pygame.image.load('../graphics/test/desert.png')
a[1, 2] = pygame.Vector2(1, 2)
print(a)

a1 = np.array([1.0, 3.5])
a2 = np.array([pygame.image.load('../graphics/test/desert.png'), pygame.image.load('../graphics/test/plains.png')])
a3 = np.array(['g', 'h'])
b = np.array([a1, a3])
print(b)
print(b.dtype)

a = np.array(['hellosss', 'good'])
print(a.dtype)
'''
d = pygame.Vector2(0, 0)
q = pygame.Vector2(1, 0)
print(d.dot(q))
print(type(d - (3, 4)))

VEC_2 = pygame.Vector2


def rect_rect(rect1, rect2):  # insired by https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other
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
        
def rect_circle(circle, rect):  # cilrcle = {'pos': tuple, 'r': int}, rect = {'pos': tuple, 'vec1':vect, 'vec2':vect} vec1, vec2 perpendicular
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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Survivorio')

        self.clock = pygame.time.Clock()

        self.rect1 = Rect((200, 200), (100, 0), (0, 50))
        #self.rect2 = Rect((500, 500), (50, 50), (-50, 50))
        self.circle = Circle((500, 500), 80)

    def run(self):
        game_run = True
        while game_run:
            # testing
            #print(self.collision_detector.Rect_Circle({'pos': (2, 2), 'r': 1}, {'pos': (0, 0), 'vec1': VEC_2(1, 1), 'vec2': VEC_2(-1, 1)}))
            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:  # checks if quit
                    pygame.quit()
                    sys.exit()

            # testing
            keys = pygame.key.get_pressed()
            direction = VEC_2()
            angle = 0
            if keys[pygame.K_w]:
                direction.y += -1
            if keys[pygame.K_s]:
                direction.y += 1
            if keys[pygame.K_d]:
                direction.x += 1
            if keys[pygame.K_a]:
                direction.x += -1
            if direction.magnitude() != 0:
                direction = direction.normalize()
            if keys[pygame.K_q]:
                angle -= 1
            if keys[pygame.K_e]:
                angle += 1
            if keys[pygame.K_c]:
                displacement = direction * 10
            else:
                displacement = direction
            if keys[pygame.K_0]:
                self.circle.move(displacement)
            if keys[pygame.K_8]:
                self.rect1.move(displacement)
                self.rect1.rotate(angle)
            '''
            if keys[pygame.K_9]:
                self.rect2.move(displacement)
                self.rect2.rotate(angle)
            '''
            self.screen.fill('blue')

            #if rect_rect(self.rect1, self.rect2):
            if rect_circle(self.circle, self.rect1):
                color = 'red'
            else: color = 'green'
            self.rect1.draw(color)
            self.circle.draw(color)
            #self.rect2.draw(color)

            pygame.display.update()

            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.clock.tick(60) 



class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.r = radius

    def move(self, disipacement):
        self.pos += disipacement

    def draw(self, color):
        pygame.draw.circle(pygame.display.get_surface(), color, self.pos, self.r)

class Rect:
    def __init__(self, pos, v1, v2):
        self.pos = VEC_2(pos)
        self.vec1 = VEC_2(v1)
        self.vec2 = VEC_2(v2)

    def move(self, disipacement):
        self.pos += disipacement

    def rotate(self, angle):
        self.vec1 = self.vec1.rotate(angle)
        self.vec2 = self.vec2.rotate(angle)

    def draw(self, color):
        pygame.draw.line(pygame.display.get_surface(), color, self.pos + self.vec1 + self.vec2, self.pos + self.vec1 - self.vec2, width = 5)
        pygame.draw.line(pygame.display.get_surface(), color, self.pos - self.vec1 + self.vec2, self.pos - self.vec1 - self.vec2, width = 5)
        pygame.draw.line(pygame.display.get_surface(), color, self.pos + self.vec2 + self.vec1, self.pos + self.vec2 - self.vec1, width = 5)
        pygame.draw.line(pygame.display.get_surface(), color, self.pos - self.vec2 + self.vec1, self.pos - self.vec2 - self.vec1, width = 5)


game = Game()
game.run()
