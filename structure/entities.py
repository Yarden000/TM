import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )



class Entity:
    # class for all the enteties: ressouces, animals...
    spawning_rates = {'desert': 1, 'plains': 0.5, 'forest': 0}

    def __init__(self, pos = (0, 0), size = 64, image = '../graphics/test/none.png'):
        self.pos = VEC_2(pos)
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image), (self.size, self.size))
        
        

    def display(self, screen, camera):
        if -self.size / 2 < self.pos.x + camera.player_displacement.x < WIDTH + self.size / 2:
            if -self.size / 2 < self.pos.y + camera.player_displacement.y < HEIGHT + self.size / 2:
                screen.blit(self.image, self.image.get_rect(center = VEC_2(self.pos + camera.player_displacement)))


    def run(self):
        pass



class Ressource(Entity):

    def __init__(self, camera):
        super().__init__(camera)



class Animal(Entity):

    def __init__(self, camera):
        super().__init__(camera)

    def move(self, movement):
        pass



class Structure(Entity):

    def __init__(self):
        super().__init__()


