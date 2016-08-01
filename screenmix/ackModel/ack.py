'''
Created on 01.08.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from ackModel.ackRect import AckRect


class Ack(GridLayout):

    # constructor
    def __init__(self, **kwargs):
        super(Ack, self).__init__(**kwargs)
        self.cols=1
        self.ackRect=AckRect()
        #default ack is the ack of the rectangle shape
        self.add_widget(self.ackRect)
        self.content=self.ackRect
        #####################################################
        #here you can add more ack's. When you add one more #
        #make sure, that the ack has a show method like the #
        #show_ack_rect                                      #
        #####################################################
    
    '''
    show the ack of the shape rectangle
    '''
    def show_ack_rect(self):
        self.remove_widget(self.content)
        self.add_widget(self.ackRect)
        self.content=self.ackRect
    
    