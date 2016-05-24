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
        self.heightValue=Label(text='height: 0.5 m',size_hint_x=None, width=100)
        sliderHeight=Slider(min=0.1, max=0.5, value=0.5)
        sliderHeight.bind(value=self.setHeight)
        self.add_widget(self.heightValue)
        self.add_widget(sliderHeight)
        #adding_material_area to manage the width-area
        self.widthValue=Label(text='width: 0.25 m',size_hint_x=None, width=100)
        sliderWidth=Slider(min=0.1, max=0.5, value=0.25)
        sliderWidth.bind(value=self.setWidth)
        self.add_widget(self.widthValue)
        self.add_widget(sliderWidth)
    
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
        self.heightValue.text='height: 0.'+str(value)+' m'
    
    '''
    the method setWidth change the width of the cs_view
    '''
    def setWidth(self, instance, value):
        self.cs.setWidth(value)
        value=int(value*100)
        self.widthValue.text='width: 0.'+str(value)+' m'