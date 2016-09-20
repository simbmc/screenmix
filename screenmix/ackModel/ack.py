'''
Created on 01.08.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from ackModel.ackRect import AckRect


class Ack(GridLayout):
    
    '''
    ack contains all acks from the different shapes. it manage which ack-should
    show in the ack-menu, which is append of the cross-section shape
    '''
    
    # all acks of the application
    ackRect = ObjectProperty()
    #####################################################
    # here you can add more ack's. When you add one more #
    # make sure, that the ack has a show method like the #
    # show_ack_rect                                      #
    #####################################################
    
    # constructor
    def __init__(self, **kwargs):
        super(Ack, self).__init__(**kwargs)
        self.cols = 1
        # default ack is the ack of the rectangle shape
        self.ackRect = AckRect()
        self.content = self.ackRect
        self.add_widget(self.content)
    
    '''
    show the ack of the shape rectangle
    '''
    def show_ack_rect(self):
        # remove the old content
        self.remove_widget(self.content)
        self.add_widget(self.ackRect)
        # safe the new ack as content
        self.content = self.ackRect
    
    
