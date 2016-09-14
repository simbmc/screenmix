'''
Created on 16.03.2016
@author: mkennert
'''
class AMaterial(object):
    
    '''
    baseclass for the materials. when you add more materials, 
    make sure that you call the constructor of this base-class
    '''
    
    # constructor
    def __init__(self, name, price, density, stiffness, strength, color):
        self.name = name
        self.price = float(price)
        self.density = float(density)
        self.stiffness = float(stiffness)
        self.strength = float(strength)
        self.color = color