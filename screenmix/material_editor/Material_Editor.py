'''
Created on 04.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from material_editor.Keyboard import Keyboard


class Material_Editor(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)
        self.cols=2
        self.create_popups()
        self.create_gui()
    
    def create_gui(self):
        name_btn=Button(text='name')
        name_btn.bind(on_press=self.use_keyboard)
        self.add_widget(Label(text='name: '))
        self.add_widget(name_btn)
        price_btn=Button(text='0.0')
        price_btn.bind(on_press=self.use_numpad)
        self.add_widget(Label(text='price: '))
        self.add_widget(price_btn)
        density_btn=Button(text='0.0')
        density_btn.bind(on_press=self.use_numpad)
        self.add_widget(Label(text='density: '))
        self.add_widget(density_btn)
        stiffness_btn=Button(text='0.0')
        stiffness_btn.bind(on_press=self.use_numpad)
        self.add_widget(Label(text='stiffness: '))
        self.add_widget(stiffness_btn)
        strength_btn=Button(text='0.0')
        strength_btn.bind(on_press=self.use_numpad)
        self.add_widget(Label(text='strength: '))
        self.add_widget(strength_btn)
    
    def create_popups(self):
        self.popup_keyboard=Popup(title='materials',content=Keyboard(),size=(20, 20))
        
    def use_keyboard(self,button):
        self.popup_keyboard.open()
    
    def use_numpad(self,button):
        pass
    
class EditorApp(App):
    def build(self):
        return Material_Editor()

if __name__ == '__main__':
    EditorApp().run()