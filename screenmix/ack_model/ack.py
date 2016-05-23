'''
Created on 15.04.2016

@author: mkennert
'''
from decimal import Decimal

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from ack_model.ack_left import Ack_Left
from ack_model.ack_right import Ack_Right


class Ack(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Ack, self).__init__(**kwargs)
        self.cols=1
    
    '''
    create the gui
    '''
    def createGui(self):
        self.strainSlider=Slider(min=1e-10, max=0.1,value=1e-5)
        self.content_ack=GridLayout(cols=2)
        self.ack_left=Ack_Left()
        self.ack_right=Ack_Right()
        self.ack_right.setAck(self)
        self.ack_left.setAck(self)
        self.ack_left.setAckRight(self.ack_right)
        self.ack_right.setAckLeft(self.ack_left)
        self.ack_left.setCrossSection(self.cs)
        self.ack_right.setCrossSection(self.cs)
        self.content_ack.add_widget(self.ack_left)
        self.content_ack.add_widget(self.ack_right)
        self.add_widget(self.content_ack)
        slider_layout=GridLayout(cols=2, row_force_default=True,
                             row_default_height=40, size_hint_y=None, height=40)
        self.strain = Label(text='strain: ',size_hint_x=None, width=200)
        slider_layout.add_widget(self.strain)
        slider_layout.add_widget(self.strainSlider)
        self.add_widget(slider_layout)
        self.strainSlider.bind(value=self.update_strain)
    
    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''
    def setCrossSection(self,cross_section):
        self.cs=cross_section
        self.createGui()
    
    '''
    update the left and the right side
    '''
    def update(self):
        self.strainSlider.value=0
        self.ack_right.update()
        self.ack_left.update()
    
    '''
    set the maximum of the slider
    '''
    def setMaxStrain(self,value):
        self.strainSlider.max=value
    
    '''
    set the label text to the current value of 
    the sliderStrain
    '''
    def update_strain(self,instance,value):
        self.strain.text='strain: '+str('%.2E' % Decimal(str(value)))
        self.ack_right.updatePlots()
        self.ack_left.setFocusPosition(value)
    
    '''
    return the current strain
    '''
    def getCurrentStrain(self):
        return self.strainSlider.value
    
    '''
    return the max strain
    '''
    def getMaxStrain(self):
        return self.strainSlider.max