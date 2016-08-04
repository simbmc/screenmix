'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod


class IView:
    '''
    iview is a interface which the views must implement. 
    '''
    
    @abstractmethod
    def add_layer(self, x, y, material):
        raise NotImplemented('not implemented')

    @abstractmethod
    def delete_layer(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def update_layer_information(self, name, price, density,
                                 stiffness, strength, percent):
        raise NotImplemented('not implemented')

    @abstractmethod
    def create_graph(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def update_cs_information(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def get_free_places(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def update_percent(self, value):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def calculate_strain_of_concrete(self):
        raise NotImplemented('not implemented')
