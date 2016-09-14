'''
Created on 04.04.2016
@author: mkennert
'''
from materials.amaterial import AMaterial

class GlassFiber(AMaterial):
    
    '''
    database for the material glassfiber
    '''
    
    # constructor
    def __init__(self):
        # name, price, density, stiffness, strength, color
        super(GlassFiber, self,).__init__('glass fiber', 2, 2660., 50000., 1000., [255, 20, 20])