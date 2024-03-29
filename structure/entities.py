import pygame, sys
from settings import *



class Entity:
    # class for all the enteties: ressouces, animals...

    def __init__(self, camera, pos = (0, 0), image = '../graphics/test/none.png'):
        displayable_entenies.append(self)
        self.screen = pygame.display.get_surface()
        self.camera = camera
        self.pos = VEC_2(pos)
        self.image = pygame.image.load(image).convert_alpha()
        

    def display(self):
        self.screen.blit(self.image, self.image.get_rect(center = int_VEC(self.pos + self.camera.player_displacement)))


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
