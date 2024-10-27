from settings import VEC_2
import pygame

class Line:

    def __init__(self, start:VEC_2, direction:VEC_2, color:tuple[int]):
        self.start = start
        self.end = start + direction
        self.color = color

    def draw(self, surface, displacement):
                pygame.draw.line(surface, self.color, displacement + self.start, displacement + self.end, width=1)


