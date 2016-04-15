'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

from materials.Carbon_Fiber import Carbon_Fiber
from materials.Concrete import Concrete
from materials.Glass_Fiber import Glass_Fiber
from materials.Steel import Steel


class Material_Editor(ScrollView):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)
        self.all_materials=[Steel(),Carbon_Fiber(),Concrete(),Glass_Fiber()]
        self.create_gui()
        
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.material_layout=GridLayout(cols=1)
        for i in self.all_materials:
            btn=Button(text=i.name,size_hint_y=None, height=40)
            btn.bind(on_press=self.show_material_information)
            self.material_layout.add_widget(btn)
        btn=Button(text='create material',size_hint_y=None, height=40)
        btn.bind(on_press=self.edit_material)
        self.material_layout.add_widget(btn)
        self.add_widget(self.material_layout)
    
    
    def show_material_information(self,button):
        pass
    
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