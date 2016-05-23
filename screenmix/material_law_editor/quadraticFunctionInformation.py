# -*- coding: utf-8 -*-
'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from material_editor.numpad import Numpad


class QuadraticFunctionInformation(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(QuadraticFunctionInformation, self).__init__(**kwargs)
        self.cols = 2
        self.focus_btn=None
        self.createInformation()
    
    '''
    create the gui
    '''
    def createInformation(self):
        self.add_widget(Label(text='function:'))
        self.add_widget(Label(text='f(x)=ax^2+bx+c'))
        self.add_widget(Label(text='a'))
        self.a_btn=Button(text='1:')
        self.a_btn.bind(on_press=self.showPopup)
        self.add_widget(self.a_btn)
        self.add_widget(Label(text='b'))        
        self.b_btn=Button(text='0')
        self.b_btn.bind(on_press=self.showPopup)
        self.add_widget(self.b_btn)
        self.add_widget(Label(text='c'))
        self.c_btn=Button(text='0')
        self.add_widget(self.c_btn)
        self.c_btn.bind(on_press=self.showPopup)
        self.h=Button(text='10')
        self.w=Button(text='10')
        self.h.bind(on_press=self.showPopup)
        self.w.bind(on_press=self.showPopup)
        self.add_widget(Label(text='height:'))
        self.add_widget(self.h)
        self.add_widget(Label(text='width'))
        self.add_widget(self.w)
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
        self.focus_btn.text=self.numpad.textinput.text
        self.popup_numpad.dismiss()
        if self.focus_btn==self.a_btn:
            self.a_btn.text=self.numpad.textinput.text
            self.editor.setA(float(self.a_btn.text))
        elif self.focus_btn==self.b_btn:
            self.b_btn.text=self.numpad.textinput.text
            self.editor.setB(float(self.b_btn.text))
        elif self.focus_btn==self.c_btn:
            self.c_btn.text=self.numpad.textinput.text
            self.editor.setC(float(self.c_btn.text))
        elif self.focus_btn==self.h:
            self.editor.setHeight(float(self.h.text))
        elif self.focus_btn==self.w:
            self.editor.setWidth(float(self.w.text))
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