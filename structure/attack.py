import pygame, sys
from settings import(
    VEC_2
)

class Attack:
    def __init__(self, entityManager):
        self.entityManager = entityManager

    def rect_attack(self, rect):
        rect.draw('red')
        region = tuple(rect.pos // self.entityManager.region_size)
        dist = 1
        enteties_hit = []
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                region_ = (region[0] + i, region[1] + j)
                if region_ in self.entityManager.regions:
                    for ent in self.entityManager.regions[region_]:
                        #print(ent.hitbox.pos, ent.hitbox.vec1, ent.hitbox.vec2)
                        collision_state, poushout = self.entityManager.collision_detector.collision(rect, ent.hitbox)
                        if collision_state:
                            enteties_hit.append(ent)
        # for testing
        for ent in enteties_hit: self.entityManager.remove_entity(ent) 

    
    def arc_attack(self, ent, point, radius_vec, angle, angle_duble=False):
        if 'inside zone':
            return True
        return False
    
    def circle_attack(self, ent, point, radius):
        if 'inside zone':
            return True
        return False