# -*- coding: utf-8 -*-
'''
Created on 11.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from cross_section.cs import Cross_Section
from material_editor.creater import Material_Creater


class Material_Editor(ScrollView):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)
        
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_material_information()
        self.material_layout=GridLayout(cols=1,spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.material_layout.bind(minimum_height=self.material_layout.setter('height'))
        for i in self.all_materials.all_materials:
            btn=Button(text=i.name,size_hint_y=None, height=40)
            btn.bind(on_press=self.show_material_information)
            self.material_layout.add_widget(btn)
        #just for demonstration
        '''
        for i in range(0,20):
            btn=Button(text=str(i),size_hint_y=None, height=40)
            self.material_layout.add_widget(btn)
        '''
        self.btn_material_editor=Button(text='create material',size_hint_y=None, height=40)
        self.btn_material_editor.bind(on_press=self.create_material)
        self.material_layout.add_widget(self.btn_material_editor)
        self.add_widget(self.material_layout)
    
    '''
    create the popups: 
    popup_info to show the material information
    popup_create to create new material
    '''
    def create_popups(self):
        creater=Material_Creater()
        creater.sign_in_parent(self)
        self.popup_info=Popup(title='material',content=self.content)
        self.popup_create=Popup(title='create new material', content=creater)
        
    '''
    create the gui which is necessary for the show of the 
    material-information
    '''
    def create_material_information(self):
        self.name=Label()
        self.price=Label()
        self.density=Label()
        self.stiffness=Label()
        self.strenght=Label()
        self.content=GridLayout(cols=2)
        self.content.add_widget(Label(text='name:'))
        self.content.add_widget(self.name)
        self.content.add_widget(Label(text='price[euro/kg]:'))
        self.content.add_widget(self.price)
        self.content.add_widget(Label(text='density[kg/m^3]:'))
        self.content.add_widget(self.density)
        self.content.add_widget(Label(text='stiffness[MPa]:'))
        self.content.add_widget(self.stiffness)
        self.content.add_widget(Label(text='strength[MPa]:'))
        self.content.add_widget(self.strenght)
        btn_back=Button(text='back')
        btn_back.bind(on_press=self.cancel_show)
        self.content.add_widget(btn_back)
        self.create_popups()
    
    #not finished yet
    def show_material_information(self,button):
        for i in range(0,self.cross_section.all_materials.get_length()):
            if self.all_materials.all_materials[i].name==button.text:
                self.name.text=self.all_materials.all_materials[i].name
                self.price.text=str(self.all_materials.all_materials[i].price)
                self.density.text=str(self.all_materials.all_materials[i].density)
                self.stiffness.text=str(self.all_materials.all_materials[i].stiffness)
                self.strenght.text=str(self.all_materials.all_materials[i].strength)
                self.popup_info.open()
    
    #not finished yet
    def cancel_show(self,button):
        self.popup_info.dismiss()
        
    #not finished yet
    def create_material(self,button):
        self.popup_create.open()
    
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''
    def update(self):
        print('here')
        self.material_layout.remove_widget(self.btn_material_editor)
        btn_material_A=Button(text=self.all_materials.all_materials[-1].name,size_hint_y=None, height=40)
        btn_material_A.bind(on_press=self.show_material_information)
        self.material_layout.add_widget(btn_material_A)
        self.material_layout.add_widget(self.btn_material_editor)
        print('material-editor:'+str(self.all_materials))
        
    #not finished yet
    def cancel_edit_material(self):
        self.popup_create.dismiss()
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,cross_section):
        self.cross_section=cross_section
        self.all_materials=self.cross_section.all_materials
        self.all_materials.add_listener(self)
        self.create_gui()
        