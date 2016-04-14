'''
Created on 11.04.2016

@author: mkennert
'''
from materials.AMaterial import AMaterial

class Own_Material(AMaterial):
    def __init__(self,name,price,density,stiffness,strength):
        super(Own_Material,self,).__init__(name, float(price),float(density),float(stiffness),float(strength))