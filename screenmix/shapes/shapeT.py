'''
Created on 03.06.2016

@author: mkennert
'''
from shapes.ashape import AShape

class ShapeT(AShape):
    # Constructor

    def __init__(self, **kwargs):
        super(ShapeT, self).__init__(**kwargs)
        self.cols = 2
        # toparea
        self.tw = 0.2
        self.th = 0.2
        # bottomarea
        self.bw = 0.3
        self.bh = 0.2
        self.concreteDensity = 2300.
        self.concretePrice = 0.065
        self.concreteStiffness = 30000.
        self.concreteStrength = 3.
        
    '''
    return the top-width
    '''

    def getWidthTop(self):
        return self.tw

    '''
    set the top-width
    '''

    def setWidthTop(self, value):
        self.tw = value
        self.view.update()

    '''
    return the top-height
    '''

    def getHeightTop(self):
        return self.th

    '''
    set the top-height
    '''

    def setHeightTop(self, value):
        self.th = value
        self.view.update()
    
    '''
    set the bottom-height
    '''

    def setHeightBottom(self, value):
        self.bh = value
        self.view.update()

    '''
    return the bottom-height
    '''

    def getHeightBottom(self):
        return self.bh

    '''
    set the bottom-width
    '''

    def setWidthBottom(self, value):
        self.bw = value
        self.view.update()

    '''
    return the bottom-width
    '''

    def getWidthBottom(self):
        return self.bw
    
    '''
    return the cs-height
    '''

    def getHeight(self):
        return self.th + self.bh
    
        '''
    return the max-width
    '''

    def getWidth(self):
        if self.tw < self.bw:
            return self.bw
        else:
            return self.tw
    