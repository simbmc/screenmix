'''
Created on 23.07.2016

@author: mkennert
'''
from abc import abstractmethod

from kivy.properties import NumericProperty, ListProperty, ObjectProperty


class ILayer:
    
    '''
    ilayer is a interface which the layers must implement. so this interface gives 
    a structure about the method which are necessary for the other components
    which use the layer
    '''
    
    # x-coordinate of the layer
    x = NumericProperty()
    
    # y-coordinate of the layer 
    y = NumericProperty()
    
    # height of the layer
    h = NumericProperty()
    
    # width of the layer
    w = NumericProperty()
    
    # percentage of the layer
    p = NumericProperty()
    
    # strain of the material
    strain = NumericProperty()
    
    # material of the layer
    material = ObjectProperty()
    
    # focus
    focus = False
    
    # color of the filled-rectangle
    colors = ListProperty()
    
    # components to show the layer in the graph
    layerCs, layerAck = ObjectProperty(), ObjectProperty()
    
    @abstractmethod
    def mouse_within(self, x, y):
        # should proof whether the touch is in 
        # the layer
        raise NotImplemented('not implemented')
    
    @abstractmethod    
    def mouse_within_x(self, x):
        # should proof whether the touch.x is in the graph
        # this is necessary to improve the move-method of
        # the layer  
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def get_weight(self):
        # should return the weight of the layer
        raise NotImplemented('not implemented')
    
    '''
    return the materials information. this method 
    does not have to implement in the layer-class
    '''
    def get_material_informations(self):
        return [self.material.name, self.material.price,
                self.material.density, self.material.stiffness,
                self.material.strength]
