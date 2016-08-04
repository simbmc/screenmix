'''
Created on 23.07.2016

@author: mkennert
'''
from abc import abstractmethod


class ILayer:
    '''
    ilayer is a interface which the layers must implement. 
    '''
    @abstractmethod
    def mouse_within(self, x, y):
        raise NotImplemented('not implemented')
    
    @abstractmethod    
    def mouse_within_x(self, x):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def get_strain(self):
        raise NotImplemented('not implemented')
    
    '''
    return the materials information
    '''

    def get_material_informations(self):
        return [self.material.name, self.material.price,
                self.material.density, self.material.stiffness,
                self.material.strength]