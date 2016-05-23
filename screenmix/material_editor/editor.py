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

from material_editor.creater import Material_Creater
from designClass.design import Design
from material_editor.iobserver import IObserver


class Material_Editor(ScrollView, IObserver):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)
        self.btnSize=Design.btnSize
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def createGui(self):
        self.createMaterialInformation()
        self.material_layout=GridLayout(cols=1,spacing=2, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.material_layout.bind(minimum_height=self.material_layout.setter('height'))
        for i in self.all_materials.all_materials:
            btn=Button(text=i.name,size_hint_y=None, height=self.btnSize)
            btn.bind(on_press=self.showMaterialInformation)
            self.material_layout.add_widget(btn)
        self.btn_material_editor=Button(text='create material',size_hint_y=None, height=self.btnSize)
        self.btn_material_editor.bind(on_press=self.createMaterial)
        self.material_layout.add_widget(self.btn_material_editor)
        self.add_widget(self.material_layout)
    
    '''
    create the popups: 
    popup_info to show the material information
    popup_create to create new material
    '''
    def createPopups(self):
        creater=Material_Creater()
        creater.signInParent(self)
        self.popup_info=Popup(title='material',content=self.content)
        self.popup_create=Popup(title='create new material', content=creater)
        
    '''
    create the gui which is necessary for the show of the 
    material-information
    '''
    def createMaterialInformation(self):
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
        btn_back.bind(on_press=self.cancelShow)
        self.content.add_widget(btn_back)
        self.createPopups()
    
    '''
    set the labeltext with the materialproperties
    '''
    def showMaterialInformation(self,button):
        for i in range(0,self.cs.all_materials.getLength()):
            if self.all_materials.all_materials[i].name==button.text:
                self.name.text=self.all_materials.all_materials[i].name
                self.price.text=str(self.all_materials.all_materials[i].price)
                self.density.text=str(self.all_materials.all_materials[i].density)
                self.stiffness.text=str(self.all_materials.all_materials[i].stiffness)
                self.strenght.text=str(self.all_materials.all_materials[i].strength)
                self.popup_info.open()
    
    '''
    close the popup, which shows the information from
    the choosen material
    '''
    def cancelShow(self,button):
        self.popup_info.dismiss()
        
    '''
    open the popup, which has the creator as content
    '''
    def createMaterial(self,button):
        self.popup_create.open()
    
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''
    def update(self):
        self.material_layout.remove_widget(self.btn_material_editor)
        btn_material_A=Button(text=self.all_materials.all_materials[-1].name,size_hint_y=None, height=40)
        btn_material_A.bind(on_press=self.showMaterialInformation)
        self.material_layout.add_widget(btn_material_A)
        self.material_layout.add_widget(self.btn_material_editor)
        
    '''
    cancel the create-process. this method 
    is necessary, because editor is the parent 
    of the creator and creator call the method cancelEditMaterial
    from the parent
    '''
    def cancelEditMaterial(self):
        self.popup_create.dismiss()
    
    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''
    def setCrossSection(self,cross_section):
        self.cs=cross_section
        self.all_materials=self.cs.all_materials
        self.all_materials.addListener(self)
        self.createGui()
        