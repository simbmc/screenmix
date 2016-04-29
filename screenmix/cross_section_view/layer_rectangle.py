'''
Created on 14.04.2016

@author: mkennert
'''


class Layer_Rectangle:
    # Constructor

    def __init__(self, x_coordinate, y_coordinate, height, width, colors, percent):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self._height = height
        self._width = width
        self.colors = colors
        self.focus = False
        self.percentage = percent
        self.filledRectCs=None
        self.filledRectAck=None
        
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''

    def mouse_within(self, x_value, y_value):
        if y_value < self.y_coordinate + self._height / 2. and y_value > self.y_coordinate - self._height / 2. and x_value > 0. and x_value < self._width:
            return True
        else:
            return False
    
    
    def mouse_within_just_x_coordinate(self, x_value):
        if x_value > 0. and x_value < self._width:
            return True
        else:
            return False
    
       
    '''
    checked wheter the layers are the same
    '''

    def equals(self, x, y, width, height):
        if self.x_coordinate == x and self.y_coordinate == y and self._height == height and self._width == width:
            return True
        else:
            return False

    '''
    the method set_height change the height of the small_keyboard-rectangle
    '''
    def set_height(self, value):
        self._height = value

    '''
    the method to change the percentage
    '''

    def set_percentage(self, value):
        self.percentage = value

    '''
    the method set_width change the width of the small_keyboard-rectangle
    '''

    def set_width(self, value):
        self._width = value

    '''
    the method set_y_coordinate change the y_coordinate of the small_keyboard-rectangle
    '''

    def set_y_coordinate(self, value):
        self.y_coordinate = value

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
        volume = self._height * self._width
        weight = self.material.density * volume
        return weight

    '''
    return the strain of the layer
    '''

    def get_strain(self):
        return self.material.strength / self.material.stiffness
    
    '''
    set the filledRectCs
    '''
    def setFilledRectCs(self, filledRect):
        self.filledRectCs=filledRect
    
    '''
    set the filledRectAck
    '''
    def setFilledRectAck(self, filledRect):
        self.filledRectAck=filledRect
    
    '''
    set the yrange
    '''
    def setYRange(self,values):
        self.filledRectAck.yrange=values
        self.filledRectCs.yrange=values