'''
Created on 15.04.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from ack_model.ACK_Left import Ack_Left
from ack_model.ACK_Right import Ack_Right

class Ack(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Ack, self).__init__(**kwargs)
        self.cols=2
    
    def create_gui(self):
        self.ack_left=Ack_Left()
        self.ack_right=Ack_Right()
        self.ack_left.set_ack_right(self.ack_right)
        self.ack_right.set_ack_left(self.ack_left)
        self.ack_left.set_cross_section(self.cross_section)
        self.ack_right.set_cross_section(self.cross_section)
        self.add_widget(self.ack_left)
        self.add_widget(self.ack_right)
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,cross_section):
        self.cross_section=cross_section
        self.create_gui()
    
    def update(self):
        self.ack_right.update()