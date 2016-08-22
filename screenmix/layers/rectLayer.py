'''
Created on 14.04.2016
@author: mkennert
'''
from kivy.properties import NumericProperty, ListProperty, ObjectProperty

from iLayer import ILayer


class RectLayer(ILayer):
    
    '''
    RectLayer represents a layer which has a shape like
    a rectangle
    '''
    
    # x-, y-coordinate of the layer
    x, y = NumericProperty(), NumericProperty()
    # height, width, procent of the layer
    h, w, p = NumericProperty(), NumericProperty(), NumericProperty()
    # strain of the material
    strain = NumericProperty()
    # color of the filled-rectangle
    colors = ListProperty()
    material = ObjectProperty()
    # components to show the layer in the graph
    layerCs, layerAck = ObjectProperty(), ObjectProperty()
    
    # Constructor
    def __init__(self, x, y, h, w, colors, p):
        self.x, self.y = x, y
        self.h, self.w, self.p = h, w, p
        self.colors = colors
        # default the layer has no focus
        self.focus = False

    '''
    check if the mouse is in the layer
    '''

    def mouse_within(self, x, y):
        if self.p<0.05:
            m=1.08
        else:
            m=1
        if y < self.layerCs.yrange[1]*m and y > self.layerCs.yrange[0] and \
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
    return the weight of the layer
    '''

    def get_weight(self):
        volume = self.h * self.w
        weight = self.material.density * volume
        return weight

    '''
    set the yrange
    '''

    def update_yrange(self, values):
        self.layerAck.yrange = values
        self.layerCs.yrange = values
