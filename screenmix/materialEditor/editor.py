# -*- coding: utf-8 -*-
'''
Created on 11.04.2016
@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from materialEditor.creater import MaterialCreater
from designClass.design import Design


class Material_Editor(ScrollView):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)
        self.btnSize=Design.btnSize
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_material_information()
        self.material_layout=GridLayout(cols=1,spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.material_layout.bind(minimum_height=self.material_layout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn=Button(text=i.name,size_hint_y=None, height=self.btnSize)
            btn.bind(on_press=self.show_material_information)
            self.material_layout.add_widget(btn)
        self.btnMaterialEditor=Button(text='create material',size_hint_y=None, height=self.btnSize)
        self.btnMaterialEditor.bind(on_press=self.create_material)
        self.material_layout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.material_layout)
    
    '''
    create the popups: 
    popup_info to show the material information
    popup_create to create new material
    '''
    def create_popups(self):
        creater=MaterialCreater()
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
        btn_back=Button(text='back',size_hint_y=None,height=self.btnSize)
        btn_back.bind(on_press=self.cancel_show)
        self.content.add_widget(btn_back)
        self.create_popups()
    
    '''
    set the labeltext with the materialproperties
    '''
    def show_material_information(self,button):
        for i in range(0,self.cs.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name==button.text:
                self.name.text=self.allMaterials.allMaterials[i].name
                self.price.text=str(self.allMaterials.allMaterials[i].price)
                self.density.text=str(self.allMaterials.allMaterials[i].density)
                self.stiffness.text=str(self.allMaterials.allMaterials[i].stiffness)
                self.strenght.text=str(self.allMaterials.allMaterials[i].strength)
                self.popup_info.open()
    
    '''
    close the popup, which shows the information from
    the choosen material
    '''
    def cancel_show(self,button):
        self.popup_info.dismiss()
        
    '''
    open the popup, which has the creator as content
    '''
    def create_material(self,button):
        self.popup_create.open()
    
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''
    def update(self):
        self.material_layout.remove_widget(self.btnMaterialEditor)
        btn_material_A=Button(text=self.allMaterials.allMaterials[-1].name,size_hint_y=None, height=40)
        btn_material_A.bind(on_press=self.show_material_information)
        self.material_layout.add_widget(btn_material_A)
        self.material_layout.add_widget(self.btnMaterialEditor)
        
    '''
    cancel the create-process. this method 
    is necessary, because editor is the parent 
    of the creator and creator call the method cancel_edit_material
    from the parent
    '''
    def cancel_edit_material(self):
        self.popup_create.dismiss()
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,cs):
        self.cs=cs
        self.allMaterials=self.cs.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
        