import pygame, sys
from settings import (
    WIDTH, 
    HEIGHT, 
    VEC_2, 
    )



class Entity:
    # class for all the enteties: ressouces, animals...

    def __init__(self, pos = (0, 0), size = 64, image = '../graphics/test/none.png'):
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
    
    def __init__(self, camera, map, chunks, displayable_entenies):
        self.camera = camera
        self.map = map
        self.chunks = chunks
        self.displayable_entenies = displayable_entenies

    def spawn_test_ent(self, pos = (0, 0), size = 64, image = '../graphics/test/none.png'):
        # test
        test_entity = Entity(pos, size, image)
        self.displayable_entenies.append(test_entity)

    def chunks_loaded(self):
        chunk_in = (int(len(self.chunks) / 2) + (WIDTH / 2 - self.camera.player_displacement[0]) // self.map.chunk_size_in_pixel), (int(len(self.chunks) / 2) + (HEIGHT / 2 - self.camera.player_displacement[1]) // self.map.chunk_size_in_pixel)
        #print(self.map.chunk_size_in_pixel)
        print(chunk_in)

class RessourceSpawner(Spawner):

    def __init__(self):
        super().__init__()



class AnimalSpawner(Spawner):

    def __init__(self):
        super().__init__()



class StructureSpawner(Spawner):

    def __init__(self):
        super().__init__()
