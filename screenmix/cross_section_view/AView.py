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
    def set_height(self,value):
        pass
    
    @abstractmethod
    def set_width(self, value):
        pass
    
    @abstractmethod
    def set_percent(self, value):
        pass
    
    @abstractmethod
    def show_add_layer_area(self, percent,name):
        pass
    
    @abstractmethod
    def delete_layer(self):
        pass
    
    def set_height(self,value):
        self.view_height=float(value)
    
    def set_width(self,value):
        self.view_width=float(value)
    
    def set_view(self, view):
        self.view=AView(view)
    
        
        