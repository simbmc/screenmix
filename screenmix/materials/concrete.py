'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class Concrete(AMaterial):
    
    '''
    database for the material concrete
    '''
    
    #constructor
    def __init__(self):
        #name, price, density, stiffness, strength, color
        super(Concrete,self,).__init__('concrete', 0.065,2300.,30000.,3.,[0,0,0])
