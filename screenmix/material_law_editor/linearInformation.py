'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from designClass.design import Design
from material_editor.numpad import Numpad


class LinearInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(LinearInformation, self).__init__(**kwargs)
        self.cols=2
        self.btnSize=Design.btnSize
        self.createGUI()
        
    '''
    create the gui
    '''
    def createGUI(self):
        self.createPopup()
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=mx+b'))
        self.add_widget(Label(text='m'))
        self.btn_m=Button(text='1',size_hint_y=None, height=self.btnSize)
        self.btn_m.bind(on_press=self.showPopup)
        self.add_widget(self.btn_m)
    
    '''
    create the popup with the numpad as content
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popup_numpad=Popup(title='Numpad', content=self.numpad)
    
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
    
    '''
    the method finishedNumpad close the numpad_popup
    '''
    def finishedNumpad(self):
        self.focus_btn.text=self.numpad.textinput.text
        self.popup_numpad.dismiss()
        if self.focus_btn==self.btn_m:
            self.focus_btn=self.btn_m
            self.btn_m.text=self.numpad.textinput.text
        self.numpad.resetText()
    