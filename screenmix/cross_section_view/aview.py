'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod


class AView(object):
    @abstractmethod
    def set_percent(self, value):
        raise NotImplemented('not implemented')

    @abstractmethod
    def add_layer(self, percent, material):
        raise NotImplemented('not implemented')

    @abstractmethod
    def delete_layer(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def update_layer_information(self, name, price, density, stiffness, strength, percent):
        raise NotImplemented('not implemented')

    @abstractmethod
    def create_graph(self):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def on_touch_move(self, touch):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def on_touch_down(self, touch):
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def set_cross_section(self, cross_section):
        raise NotImplemented('not implemented')