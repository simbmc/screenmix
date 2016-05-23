'''
Created on 06.05.2016

@author: mkennert
'''

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from material_editor.numpad import Numpad


class MultilinearInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(MultilinearInformation, self).__init__(**kwargs)
        self.cols = 2
        self.btnSize=Design.btnSize
        self.focus_btn=None
        self.create_information()
    
    '''
    create the gui of the information
    '''
    def create_information(self):
        self.add_widget(Label(text='function:',size_hint_x=None, width=200))
        self.add_widget(Label(text='multilinear',size_hint_x=None, width=200))
        self.points_lbl=Label(text='points:',size_hint_x=None, width=200)
        self.points_btn=Button(text='5',size_hint_y=None, height=self.btnSize)
        self.points_btn.bind(on_press=self.showPopup)
        self.height_lbl=Label(text='height:',size_hint_x=None, width=200)
        self.height_btn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.height_btn.bind(on_press=self.showPopup)
        self.width_lbl=Label(text='width:',size_hint_x=None, width=200)
        self.width_btn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.width_btn.bind(on_press=self.showPopup)
        self.add_widget(self.points_lbl)
        self.add_widget(self.points_btn)
        self.add_widget(self.height_lbl)
        self.add_widget(self.height_btn)
        self.add_widget(self.width_lbl)
        self.add_widget(self.width_btn)
        self.createPopup()
    
    '''
    create the popup with the numpad as content
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popup_numpad=Popup(title='Numpad', content=self.numpad)
    
    '''
    the method finishedNumpad close the numpad_popup
    '''
    def finishedNumpad(self):
        self.popup_numpad.dismiss()
        if self.focus_btn==self.points_btn:
            self.points_btn.text=self.numpad.textinput.text
            print(self.points_btn.text)
            self.editor.setPoints(float(self.points_btn.text))
        elif self.focus_btn==self.width_btn:
            self.width_btn.text=self.numpad.textinput.text
            self.editor.setWidth(float(self.width_btn.text))
        elif self.focus_btn==self.height_btn:
            self.height_btn.text=self.numpad.textinput.text
            self.editor.setHeight(float(self.height_btn.text))
        self.numpad.resetText()
    
    '''
    open the numpad popup
    '''
    def showPopup(self,btn):
        self.focus_btn=btn
        self.popup_numpad.open()
    
    '''
    sign in by the parent
    '''
    def signIn(self, parent):
        self.editor=parent
    
    