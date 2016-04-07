'''
Created on 16.03.2016

@author: mkennert
'''
from abc import abstractmethod
class AMaterial(object):
    #Constructor
    def __init__(self, name, price, density,stiffness, strength):
        self.name=str(name)
        self.price=float(price)
        self.density=float(density)
        self.stiffness=float(stiffness)
        self.strength=float(strength)
    
    def set_name(self, name):
        self.name=str(name)
    
    def get_name(self):
        return self.name
    
    def set_price(self, price):
        self.price=float(price)
    
    def get_price(self,):
        return self.price
    
    def set_density(self, density):
        self.density=float(density)
    
    def get_density(self):
        return self.density
    
    def set_stiffness(self, stiffness):
        self.stiffness=float(stiffness)
    
    def get_stiffness(self):
        return self.stiffness
    
    def set_strength(self, strength):
        self.strength=float(strength)
    
    def get_strength(self):
        return self.strength
    
    @abstractmethod
    def calculate_price(self):
        pass
    
    @abstractmethod
    def calculate_stiffness(self):
        pass
    
    @abstractmethod
    def calculate_density(self):
        pass
    
    @abstractmethod
    def calculate_weight(self):
        pass
    
    @abstractmethod
    def calculate_strength(self):
        pass
        