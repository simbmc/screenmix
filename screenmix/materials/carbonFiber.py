'''
Created on 04.04.2016
@author: mkennert
'''
from materials.amaterial import AMaterial

class CarbonFiber(AMaterial):
    
    '''
    database for the material carbonfiber
    '''
    
    #constructor
    def __init__(self):
        #name, price, density, stiffness, strength, color
        super(CarbonFiber,self,).__init__('carbon fiber', 20,1600,250000,1600,[140, 255, 102])