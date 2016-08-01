'''
Created on 16.03.2016

@author: mkennert
'''
from kivy.properties import NumericProperty


class AMaterial(object):

    # Constructor
    def __init__(self, name, price, density, stiffness, strength,color):
        self.name = str(name)
        self.price, self.density = float(price), float(density)
        self.stiffness, self.strength = float(stiffness), float(strength)
        self.color=color
    
    