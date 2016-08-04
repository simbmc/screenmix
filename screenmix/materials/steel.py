'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class Steel(AMaterial):
    '''
    database for the material steel
    '''
    
    # constructor
    def __init__(self):
        # name, price, density, stiffness, strength, color
        super(Steel, self,).__init__('steel', 0.35, 7850., 210000., 350., [100, 100, 255])
