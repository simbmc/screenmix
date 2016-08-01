'''
Created on 23.07.2016

@author: mkennert
'''
from abc import abstractmethod


class ILayer:
    @abstractmethod
    def mouse_within(self, x, y):
        raise NotImplemented('not implemented')
    
    @abstractmethod    
    def mouse_within_x(self, x):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def set_layer_ack(self, filledRect):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def set_layer_cs(self, filledRect):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def get_material_informations(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def set_material(self, material):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def get_strain(self):
        raise NotImplemented('not implemented')
        