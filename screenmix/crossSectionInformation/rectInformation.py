'''
Created on 26.07.2016

@author: mkennert
'''

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class RectangleInformation(GridLayout):
    
    '''
    create the component, where you can change the height and 
    the width of the cross-section-rectangle
    '''
    
    # cross section shape - rectangle
    cs = ObjectProperty()
    
    heightStr = StringProperty('height [m]')
    
    widthStr = StringProperty('width [m]')
    
    # constructor
    def __init__(self, **kwargs):
        super(RectangleInformation, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.size_hint_y = None
        
    '''
    create the gui
    '''

    def create_gui(self):
        # create the area where you can scale the height
        # and the width of the cross section
        self.btnheight = OwnButton(text=str(self.cs.h))
        self.btnwidth = OwnButton(text=str(self.cs.w))
        self.add_widget(OwnLabel(text=self.heightStr))
        self.add_widget(self.btnheight)
        self.add_widget(OwnLabel(text=self.widthStr))
        self.add_widget(self.btnwidth)
        self.btnheight.bind(on_press=self.show_numpad)
        self.btnwidth.bind(on_press=self.show_numpad)
        # create the numpad, where you can input values
        self.numpad = Numpad(p=self)
        self.popupNumpad = OwnPopup(content=self.numpad)

    '''
    show the numpad for the input.
    '''

    def show_numpad(self, btn):
        self.popupNumpad.open()
        self.btnFocus = btn
        if self.btnFocus == self.btnheight:
            self.popupNumpad.title = self.heightStr
        else:
            self.popupNumpad.title = self.widthStr
    
    '''
    close the numpad when the user confirm the input
    and update the components
    '''

    def finished_numpad(self):
        v = float(self.numpad.lblTextinput.text)
        self.btnFocus.text = str(v)
        if self.btnFocus == self.btnheight:
            self.cs.update_height(v)
        else:
            self.cs.update_width(v)
        self.popupNumpad.dismiss()
    
    '''
    close the numpad, when the user cancel the input
    '''

    def close_numpad(self):
        self.popupNumpad.dismiss()
