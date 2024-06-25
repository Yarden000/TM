'''camera'''
from settings import (
    WIDTH,
    HEIGHT,
    VEC_2
    )


class Camera:
    '''
    responsible for moving everything in responce to the player movement
    '''

    def __init__(self) -> None:
        self.player_displacement = VEC_2(WIDTH/2, HEIGHT/2)
        self.true_player_displacement = VEC_2()
