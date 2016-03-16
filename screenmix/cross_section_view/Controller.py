'''
Created on 15.03.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.widget import Widget

from cross_section_view.CS_Rectangle_View import CS_Rectangle_View
#from cross_section_view.Cross_Section_Information import Cross_Section_Information
from cross_section_view import AView


'''
the Controller was developed to undock the cs_information from the view
'''
class Controller(Widget): 
    #Constructor
    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.view=CS_Rectangle_View()
    
    '''not finished yet
    def set_view(self, view):
        self.view=AView(view)
    '''
    
    '''
    the method change_height changes the height of the view
    '''
    def change_height(self,value):
        self.view.change_height(value)
    
    '''
    the method change_width change the width of the view
    ''' 
    def change_width(self,value):
        self.view.change_width(value)
    
    '''
    the method change_percent change the percentage share of the selected material
    '''
    def change_percent(self, value):
        pass
        #self.view.change_percent(value)
    
    '''
    the method add_material add new material in the view
    '''
    def add_material(self,percent,name):
        self.view.add_material(percent, name)
        
    
    '''
    the method delete_material delete the selected material
    '''
    def delete_material(self):
        self.view.delete_material()
    