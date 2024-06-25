'''
inspired by: https://www.youtube.com/watch?v=6BrZryMz-ac&t=334s   25 juin


Idea:
    When an animal sees something it will have a an array of vector geometriesthat will be created
    in response that are combined in proportion to their weigths. It will 'chose' a direction based 
    on the resultant vector geometry. Every thing an animal can see has an array 'activation function'
    and weights, it will either combine or choose a function based on the weights and 'pass' the norm
    of the direction-vector 'throught the 'activation function' ade the result will be the 'want' of the
    animal to go in that direction. Then it will 'choose'/combine the wants based on their weights and 
    the result will be the direction the creature will go.

All weights will be passed on hereditairly with random mutations. (Evolution!!!)
'''


class Sight:
    '''what an entity can see, maybe ray-tracing'''

class Geometries:
    '''diffrent vector geometries'''


class ActivationFunctions:
    '''
    to be used on the vector geometries
    for example: when close important but when far less important
    '''