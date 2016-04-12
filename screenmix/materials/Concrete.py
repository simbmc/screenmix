'''
Created on 04.04.2016

@author: mkennert
'''
from materials.AMaterial import AMaterial

class Concrete(AMaterial):
    def __init__(self):
        super(Concrete,self,).__init__('concrete', 0.065,2300.,30000.,3.)


        