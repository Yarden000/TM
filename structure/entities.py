import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )



class Entity:
    # class for all the enteties: ressouces, animals...

    def __init__(self, displayable_entenies, pos = (0, 0), size = 64, image = '../graphics/test/none.png'):
        displayable_entenies.append(self)
        self.screen = pygame.display.get_surface()
        self.pos = VEC_2(pos)
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image), (self.size, self.size))
        
        

    def display(self, camera):
        if -self.size / 2 < self.pos.x + camera.player_displacement.x < WIDTH + self.size / 2:
            if -self.size / 2 < self.pos.y + camera.player_displacement.y < HEIGHT + self.size / 2:
                self.screen.blit(self.image, self.image.get_rect(center = VEC_2(self.pos + camera.player_displacement)))
                print(self.pos + camera.player_displacement)


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


##############################################################
        

class Spawner:
    pass


class RessourceSpawner(Spawner):

    def __init__(self):
        super().__init__()



class AnimalSpawner(Spawner):

    def __init__(self):
        super().__init__()



class StructureSpawner(Spawner):

    def __init__(self):
        super().__init__()
