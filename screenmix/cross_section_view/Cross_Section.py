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
the Cross_Section was developed to undock the cs_information from the view
'''
class Cross_Section(Widget): 
    #Constructor
    def __init__(self, **kwargs):
        super(Cross_Section, self).__init__(**kwargs)
        self.view=CS_Rectangle_View()
    
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
        self.view.change_percent(value)
    
    '''
    the method add_layer add new material in the view
    '''
    def add_layer(self,percent):
        self.view.add_layer(percent)
    
    '''
    the method delete_layer delete the selected material
    '''
    def delete_layer(self):
        self.view.delete_layer()
    