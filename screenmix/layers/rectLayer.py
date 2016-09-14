'''
Created on 14.04.2016
@author: mkennert
'''

from iLayer import ILayer


class RectLayer(ILayer):
    
    '''
    RectLayer represents a layer which has a shape like
    a rectangle
    '''
    
    # Constructor
    def __init__(self, x, y, h, w, colors, p):
        self.x, self.y = x, y
        self.h, self.w, self.p = h, w, p
        self.colors = colors

    '''
    check if the mouse is in the layer
    '''

    def mouse_within(self, x, y, d):
        if self.p < 0.05:
            m = 1.08
        else:
            m = 1
        if self.p < 0.01:
            if self.y + d > y and y > self.y - d and x < self.w:
                return True
        elif y < self.layerCs.yrange[1] * m and y > self.layerCs.yrange[0] and \
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
