'''
Created on 26.07.2016

@author: mkennert
'''

from kivy.uix.gridlayout import GridLayout

from ownComponents.design import Design
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class RectangleInformation(GridLayout):
    # constructor

    def __init__(self, **kwargs):
        super(RectangleInformation, self).__init__(**kwargs)
        self.cols = 2
        self.btnHeight = Design.btnHeight
        self.spacing = 2
        self.focusbtn = None

    '''
    create the gui
    '''

    def create_gui(self):
        self.create_numpad()
        self.create_scale_area()

    '''
    the method create_scale_area create the area where you can 
    scale the height and the width of the cs_view
    '''

    def create_scale_area(self):
        self.btnheight = OwnButton(text='0.5')
        self.btnwidth = OwnButton(text='0.25')
        self.add_widget(OwnLabel(text='height [m]'))
        self.add_widget(self.btnheight)
        self.add_widget(OwnLabel(text='width [m]'))
        self.add_widget(self.btnwidth)
        self.btnheight.bind(on_press=self.show_numpad)
        self.btnwidth.bind(on_press=self.show_numpad)
        


    '''
    create the numpad
    '''

    def create_numpad(self):
        self.numpad = Numpad()
        self.numpad.sign_in_parent(self)
        self.popupNumpad = OwnPopup(content=self.numpad)

    '''
    show the numpad for the input
    '''

    def show_numpad(self, btn):
        self.popupNumpad.open()
        self.btnFocus = btn

    '''
    close the numpad 
    '''

    def closeNumpad(self):
        self.popupNumpad.dismiss()

    '''
    finish the numpad
    '''

    def finished_numpad(self):
        self.btnFocus.text = self.numpad.lblTextinput.text
        if self.btnFocus == self.btnheight:
            self.cs.set_height(float(self.btnFocus.text))
        else:
            self.cs.set_width(float(self.btnFocus.text))
        self.popupNumpad.dismiss()

    '''
    the method set_height change the height of the cs_view
    '''

    def set_height(self, instance, value):
        self.cs.set_height(value)
        value = int(value * 100)
        self.lblHeight.text = 'height: 0.' + str(value) + ' m'

    '''
    the method set_width change the width of the cs_view
    '''

    def set_width(self, instance, value):
        self.cs.set_width(value)
        value = int(value * 100)
        self.lblWidth.text = 'width: 0.' + str(value) + ' m'

    '''
    sign in by the cross section
    '''
    def set_cross_section(self, cs):
        self.cs = cs
        self.create_gui()
        
