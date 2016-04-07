'''
Created on 01.03.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class NumPad(Popup):
    #Construktor
    def __init__(self, **kwargs):
        super(NumPad, self).__init__(**kwargs)
        self.create_numfield()
        self.content=self.layout
        self.title='Numpad'
    
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
        
    def appending(self,button): 
        self.textinput.text+=button.text

    def delete(self,button):
        self.textinput.text=self.textinput.text[:-1]
    
    def reset_text(self):
        self.textinput.text=''
    
    def finished(self,button):
        self.dismiss()
    
class NumPadApp(App):
    def build(self):
        return NumPad()

if __name__ == '__main__':
    NumPadApp().run()