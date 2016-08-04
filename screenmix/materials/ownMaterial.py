'''
Created on 11.04.2016

@author: mkennert
'''
import random

from materials.amaterial import AMaterial


class OwnMaterial(AMaterial):
    '''
    database for ownmaterials. the values must given the 
    constructor. the own-material get a random-color
    '''
    
    # constructor
    def __init__(self, name, price, density, stiffness, strength):
        super(OwnMaterial, self,).__init__(name, price, density,
                                          stiffness, strength, 
                                          [random.randint(0, 255) for i in range(3)])
