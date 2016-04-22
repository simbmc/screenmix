'''
Created on 18.04.2016

@author: mkennert
'''
from materials.steel import Steel
from materials.carbon_fiber import Carbon_Fiber
from materials.concrete import Concrete
from materials.glass_fiber import Glass_Fiber

'''

'''
class MaterialList:
    def __init__(self):
        self.all_materials=[Steel(),Carbon_Fiber(),Concrete(),Glass_Fiber()]
        self.listeners=[]
        
    def add_Material(self, material):
        self.all_materials.append(material)
        self.update()
        
    '''
    update all listeners when a new material was added
    '''
    def update(self):
        for listener in self.listeners:
            listener.update()
    
    def add_listener(self,listener):
        self.listeners.append(listener)
    
    def get_length(self):
        return len(self.all_materials)