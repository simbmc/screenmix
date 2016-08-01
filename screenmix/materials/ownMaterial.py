'''
Created on 11.04.2016

@author: mkennert
'''
import random

from materials.amaterial import AMaterial


class OwnMaterial(AMaterial):
    #constructor
    def __init__(self,name,price,density,stiffness,strength):
        c=[random.randint(0, 255) for i in range(3)]
        print(c)
        super(OwnMaterial,self,).__init__(name, price,density,
                                          stiffness,strength,c)