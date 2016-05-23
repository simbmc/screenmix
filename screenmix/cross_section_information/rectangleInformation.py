'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
class RectangleInformation(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(RectangleInformation, self).__init__(**kwargs)
        self.cols=2
    
    '''
    create the gui
    '''
    def createGUI(self):
        #adding_material_area to manage the height-area
        self.height_value=Label(text='height: 0.5 m',size_hint_x=None, width=100)
        slider_height=Slider(min=0.1, max=0.5, value=0.5)
        slider_height.bind(value=self.setHeight)
        self.add_widget(self.height_value)
        self.add_widget(slider_height)
        #adding_material_area to manage the width-area
        self.width_value=Label(text='width: 0.25 m',size_hint_x=None, width=100)
        slider_width=Slider(min=0.1, max=0.5, value=0.25)
        slider_width.bind(value=self.setWidth)
        self.add_widget(self.width_value)
        self.add_widget(slider_width)
    
    '''
    set the cross-section
    '''
    def setCrossSection(self,crossSection):
        self.cs=crossSection
        self.createGUI()
    
    '''
    the method setHeight change the height of the cs_view
    '''
    def setHeight(self, instance, value):
        self.cs.setHeight(value)
        value=int(value*100)
        self.height_value.text='height: 0.'+str(value)+' m'
    
    '''
    the method setWidth change the width of the cs_view
    '''
    def setWidth(self, instance, value):
        self.cs.setWidth(value)
        value=int(value*100)
        self.width_value.text='width: 0.'+str(value)+' m'