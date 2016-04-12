'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class Material_Editor(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)
        self.cols=2
        self.create_gui()
        self._parent=None
        self.focus_btn=None
    
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_slider()
        self.add_widget(Label(text='name: '))
        self.name_label=Label(text='name')
        self.add_widget(self.name_label)
        self.add_widget(Label(text='price: '))
        self.add_widget(self.slider_price)
        self.add_widget(Label(text='density: '))
        self.add_widget(self.slider_density)
        self.add_widget(Label(text='stiffness: '))
        self.add_widget(self.slider_stiffness)
        self.add_widget(Label(text='strength: '))
        self.add_widget(self.slider_strength)
        self.create_btn=Button(text='create')
        self.create_btn.bind(on_press=self.edit_material)
        self.cancel_btn=Button(text='cancel')
        self.cancel_btn.bind(on_press=self.cancel)
        self.add_widget(self.cancel_btn)
        self.add_widget(self.create_btn)
    
    '''
    the method create_slider create all sliders of the class
    '''
    def create_slider(self):
        #materialprice
        self.slider_price=Slider(min=0,max=100,value=50)
        #materialdensity
        self.slider_density=Slider(min=0,max=100,value=50)
        #materialstiffness
        self.slider_stiffness=Slider(min=0,max=100,value=50)
        #materialstrength
        self.slider_strength=Slider(min=0,max=100,value=50)
    
    def edit_material(self,button):
        pass
    
    def cancel(self,button):
        pass
    
    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method update_materials
    '''
    def sign_in_parent(self, parent):
        self._parent=parent
    
class EditorApp(App):
    def build(self):
        return Material_Editor()

if __name__ == '__main__':
    EditorApp().run()