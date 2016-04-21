'''
Created on 18.04.2016

@author: mkennert
'''
from materials.Steel import Steel
from materials.Carbon_Fiber import Carbon_Fiber
from materials.Concrete import Concrete
from materials.Glass_Fiber import Glass_Fiber

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