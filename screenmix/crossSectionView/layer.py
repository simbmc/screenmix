'''
Created on 06.06.2016

@author: mkennert
'''
'''
Created on 14.04.2016
@author: mkennert
'''


class Layer:
    # Constructor

    def __init__(self, x, y, h, w, colors, p):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.colors = colors
        self.focus = False
        self.p = p
        self.layerCs=None
        self.layerAck=None
        
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''

    def mouse_within(self, x, y):
        if y < self.y + self.h / 2. and y > self.y - self.h / 2. and x > 0. and x < self.w:
            return True
        else:
            return False
    
    
    def mouse_within_x(self, x):
        if x > 0. and x < self.w:
            return True
        else:
            return False
    

    '''
    the method set_height change the height of the small_keyboard-rectangle
    '''
    def set_height(self, value):
        self.h = value

    '''
    the method to change the p
    '''

    def set_percent(self, value):
        self.p = value

    '''
    the method set_width change the width of the small_keyboard-rectangle
    '''

    def set_width(self, value):
        self.w = value

    '''
    the method set_y change the y of the small_keyboard-rectangle
    '''

    def set_y(self, value):
        self.y = value

    '''
    the method set_material was developed to set the small_keyboard the materials
    '''

    def set_material(self, material):
        self.material = material

    '''
    return the materials information
    '''

    def get_material_informations(self):
        return [self.material.name, self.material.price, self.material.density, self.material.stiffness, self.material.strength]

    '''
    return the weight of the layer
    '''

    def get_weight(self):
        volume = self.h * self.w
        weight = self.material.density * volume
        return weight

    '''
    return the strain of the layer
    '''

    def get_strain(self):
        return self.material.strength / self.material.stiffness
    
    '''
    set the layerCs
    '''
    def set_layer_cs(self, filledRect):
        self.layerCs=filledRect
    
    '''
    set the layerAck
    '''
    def set_layer_ack(self, filledRect):
        self.layerAck=filledRect
    
    '''
    set the yrange
    '''
    def set_yrange(self,values):
        self.layerAck.yrange=values
        self.layerCs.yrange=values