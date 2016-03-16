'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod
from cross_section_view.CS_Rectangle_View import CS_Rectangle_View


class AView(object):
    #Constructor
    def __init__(self):
        self.cs_view_height =0.25 
        self.cs_view_height = 0.25
        self.view=CS_Rectangle_View()
        
    @abstractmethod
    def change_height(self,value):
        pass
    
    @abstractmethod
    def change_width(self, value):
        pass
    
    @abstractmethod
    def change_percent(self, value):
        pass
    
    @abstractmethod
    def add_material(self, percent,name):
        pass
    
    @abstractmethod
    def delete_material(self):
        pass
    
    def set_height(self,value):
        self.view_height=float(value)
    
    def set_width(self,value):
        self.view_width=float(value)
    
    def set_view(self, view):
        self.view=AView(view)
    
        
        