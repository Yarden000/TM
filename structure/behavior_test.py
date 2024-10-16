import math
from settings import (
    VEC_2,
    angle_between_vectors_0_to_2pi,
    angle_between_vectors_plus_minus_pi
)


class Behavior:
    '''where all the behavior calculations are done'''
    def __init__(self, entity_manager, ent) -> None:
        self.entity_manager = entity_manager
        self.entity = ent
        self.Sight = Sight(ent)
        self.Geometries = Geometries(16)
        self.ActivationFunctions = ActivationFunctions()
        self.Averages = Averages()
        self.StateCalc = StateCalc()

    def want(self) -> tuple():
        '''gives the things an entity wants to do, (a direction to move in, and an action to do)'''
        raise ValueError('not implemented')

    def direction_after_col(self):
        raise ValueError('not implemented')



class StateCalc:
    '''claculates the state an entity is going to be in'''
    def __init__(self):
        pass

    def curent_state(self, past_state, strengt_list):
        raise ValueError('curent_state not yet implemented')
    
