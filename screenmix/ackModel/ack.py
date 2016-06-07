'''
Created on 15.04.2016
@author: mkennert
'''
from decimal import Decimal

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from ackModel.ackLeft import AckLeft
from ackModel.ackRight import AckRight


class Ack(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Ack, self).__init__(**kwargs)
        self.cols=1
    
    def create_gui(self):
        self.strainSlider=Slider(min=1e-10, max=0.1,value=1e-5)
        self.contentAck=GridLayout(cols=2)
        self.ackLeft=AckLeft()
        self.ackRight=AckRight()
        self.ackRight.set_ack(self)
        self.ackLeft.set_ack(self)
        self.ackLeft.set_ack_right(self.ackRight)
        self.ackRight.set_ack_left(self.ackLeft)
        self.ackLeft.set_cross_section(self.cs)
        self.ackRight.set_cross_section(self.cs)
        self.contentAck.add_widget(self.ackLeft)
        self.contentAck.add_widget(self.ackRight)
        self.add_widget(self.contentAck)
        sliderLayout=GridLayout(cols=2, row_force_default=True,
                             row_default_height=40, size_hint_y=None, height=40)
        self.strain = Label(text='strain: ',size_hint_x=None, width=200)
        sliderLayout.add_widget(self.strain)
        sliderLayout.add_widget(self.strainSlider)
        self.add_widget(sliderLayout)
        self.strainSlider.bind(value=self.update_strain)
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,cs):
        self.cs=cs
        self.create_gui()
    
    '''
    update the left and the right side
    '''
    def update(self):
        self.strainSlider.value=0
        self.ackRight.update()
        self.ackLeft.update()
    
    '''
    set the maximum of the slider
    '''
    def set_maxStrain(self,value):
        self.strainSlider.max=value
    
    '''
    set the label text to the current value of 
    the sliderStrain
    '''
    def update_strain(self,instance,value):
        self.strain.text='strain: '+str('%.2E' % Decimal(str(value)))
        self.ackRight.update_plots()
        self.ackLeft.set_focus_position(value)
    
    '''
    return the current strain
    '''
    def get_currentStrain(self):
        return self.strainSlider.value
    
    '''
    return the maximum strain
    '''
    def get_maxStrain(self):
        return self.strainSlider.max