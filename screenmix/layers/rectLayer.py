'''
Created on 14.04.2016
@author: mkennert
'''
from kivy.properties import NumericProperty, ListProperty, ObjectProperty

from iLayer import ILayer


class RectLayer(ILayer):
    x, y = NumericProperty(), NumericProperty()
    h, w, p = NumericProperty(), NumericProperty(), NumericProperty()
    colors = ListProperty([255, 255, 255])
    material = ObjectProperty()
    # Constructor
    def __init__(self, x, y, h, w, colors, p):
        self.x, self.y = x, y
        self.h, self.w, self.p = h, w, p
        self.colors = colors
        self.focus = False

    '''
    check if the mouse is in the layer
    '''

    def mouse_within(self, x, y):
        if y < self.layerCs.yrange[1] + self.h / 2. and y > self.layerCs.yrange[0] and \
        x > self.layerCs.xrange[0] and x < self.layerCs.xrange[1]:
            return True
        else:
            return False

    '''
    check if the mouse is in the between 0 and the layer width
    '''

    def mouse_within_x(self, x):
        if x > 0. and x < self.w:
            return True
        else:
            return False
        
    '''
    return the strain of the layer
    '''

    def get_strain(self):
        return self.material.strength / self.material.stiffness
    
    '''
    the method set_material was developed to set the small_keyboard the materials
    '''

    def set_material(self, material):
        self.material = material
    
    '''
    return the materials information
    '''

    def get_material_informations(self):
        return [self.material.name, self.material.price,
                self.material.density, self.material.stiffness,
                self.material.strength]
        
    '''
    return the weight of the layer
    '''

    def get_weight(self):
        volume = self.h * self.w
        weight = self.material.density * volume
        return weight

    '''
    set the layerCs
    '''

    def set_layer_cs(self, filledRect):
        self.layerCs = filledRect

    '''
    set the layerAck
    '''

    def set_layer_ack(self, filledRect):
        self.layerAck = filledRect

    '''
    set the yrange
    '''

    def set_yrange(self, values):
        self.layerAck.yrange = values
        self.layerCs.yrange = values