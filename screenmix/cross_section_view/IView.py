'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod


class AView(object):
    def __init__(self, view):
        self.view=view
        
    @abstractmethod
    def change_height_test(self):
        pass
    
    @abstractmethod
    def change_width_test(self):
        pass
    
    def set_height(self,value):
        self.view_height=float(value)
    
    def set_width(self,value):
        self.view_width=float(value)
        
        