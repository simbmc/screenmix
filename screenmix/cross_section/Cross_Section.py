'''
Created on 15.03.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.widget import Widget

from cross_section_view.CS_Rectangle_View import CS_Rectangle_View
from cross_section_view import AView
from cross_section_view.Cross_Section_Information import Cross_Section_Information
from kivy.uix.gridlayout import GridLayout


'''
the cross_Section was developed to undock the cs_information from the view
'''
class Cross_Section(GridLayout): 
    #Constructor
    def __init__(self, **kwargs):
        super(Cross_Section, self).__init__(**kwargs)
        self.view=CS_Rectangle_View()
        self.information=Cross_Section_Information()
        self.cols=2
        self.add_widget(self.view)
        self.add_widget(self.information)
        self.view.set_cross_section(self)
        self.information.set_cross_section(self)
    
    '''
    the method add_layer add new materials in the view
    '''
    def add_layer(self,percent):
        self.view.add_layer(percent)
    
    '''
    the method delete_layer delete the selected materials
    '''
    def delete_layer(self):
        self.view.delete_layer()
        
    '''
    the method set_layer_information update the cross section information
    after a layer get the focus
    '''
    def set_layer_information(self,name,price,density,stiffness,strength,percent):
        self.information.update_layer_information(name,price,density,stiffness,strength,percent)
    
    '''
    get all the layers
    '''
    def get_layers(self):
        return self.view.get_layers()
    
    '''
    the method set_height changes the height of the view
    '''
    def set_height(self,value):
        self.view.set_height(value)
    
    '''
    the method set_width change the width of the view
    ''' 
    def set_width(self,value):
        self.view.set_width(value)
    
    '''
    the method set_percent change the percentage share of the selected materials
    '''
    def set_percent(self, value):
        self.view.set_percent(value)