'''
Created on 01.03.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class NumPad(GridLayout):
    #Construktor
    def __init__(self, **kwargs):
        super(NumPad, self).__init__(**kwargs)
        self.create_numfield()
        self.cols=1
        self.add_widget(self.layout)
        self._parent=None
    
    '''
    the method create_numfield create the gui
    of the numpad
    '''
    def create_numfield(self):
        self.textinput=Label(text='')
        self.layout=GridLayout(cols=1)
        self.numfield=GridLayout(cols=3)
        for i in range(1,10):
            cur=Button(text=str(i))
            cur.bind(on_press=self.appending)
            self.numfield.add_widget(cur)
        btn_dot=Button(text='.')
        btn_dot.bind(on_press=self.appending)
        self.numfield.add_widget(btn_dot)
        btn_zero=Button(text='0')
        btn_zero.bind(on_press=self.appending)
        btn_delete=Button(text='<<')
        btn_delete.bind(on_press=self.delete)
        self.numfield.add_widget(btn_zero)
        self.numfield.add_widget(btn_delete)
        cur=GridLayout(cols=1)
        btn_finished=Button(text='finished')
        btn_finished.bind(on_press=self.finished)
        cur.add_widget(btn_finished)
        cur.add_widget(self.textinput)
        self.layout.add_widget(cur)
        self.layout.add_widget(self.numfield)
    
    '''
    the method appending appends the choosen digit at the end.
    the method is called when the user use the keyboard
    '''
    def appending(self,button): 
        self.textinput.text+=button.text
    
    '''
    the method delete delete the digit at the end.
    the method is called when the press the button '<<'
    '''
    def delete(self,button):
        self.textinput.text=self.textinput.text[:-1]
    
    '''
    the method reset_text reset the text of the label
    the method must be called from the developer when
    the text must be deleted
    '''
    def reset_text(self):
        self.textinput.text=''
    
    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method finished_numpad
    '''
    def sign_in_parent(self, parent):
        self._parent=parent
    
    '''
    the method finished close the popup when the user
    is finished and press the button 'finished'
    '''
    def finished(self,button):
        self._parent.finished_numpad()
    