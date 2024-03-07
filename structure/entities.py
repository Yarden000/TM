import pygame, sys
from settings import *



class Entity:
    # class for all the enteties: ressouces, animals...

    def __init__(self, pos = (0, 0), image = '../graphics/test/none.png'):
        displayable_entenies.append(self)
        self.screen = pygame.display.get_surface()
        self.pos = VEC_2(pos)
        self.image = pygame.image.load(image).convert_alpha()

    def display(self):
        print(player_displacement)
        self.screen.blit(self.image, self.image.get_rect(center = int_VEC(self.pos + player_displacement)))


    def run(self):
        pass



class Ressource(Entity):

    def __init__(self):
        super().__init__()



class Animal(Entity):

    def __init__(self):
        super().__init__()
        self.real_pos = self.pos

    def move(self, movement):
        pass



class Structure(Entity):

    def __init__(self):
        super().__init__()


##############################################################
        

class Spawner:
    pass


class Ressource_Spawner(Spawner):

    def __init__(self):
        super().__init__()



class Animal_Spawner(Spawner):

    def __init__(self):
        super().__init__()



class Structure_Spawner(Spawner):

    def __init__(self):
        super().__init__()
