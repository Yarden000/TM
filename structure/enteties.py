import pygame, sys
from settings import *



class Entety:
    # class for all the enteties: ressouces, animals...

    def __init__(self):
        displayable_entenies.append(self)
        self.pos = VEC_2()
        self.image = None
        self.rect = None

    def display(self):
        pass

    def run(self):
        pass



class Ressource(Entety):

    def __init__(self):
        super().__init__()



class Animal(Entety):

    def __init__(self):
        super().__init__()



class Structure(Entety):

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
