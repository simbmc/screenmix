'''
Created on 04.04.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from material_editor.keyboard import Keyboard
from material_editor.numpad import Numpad
from materials.own_material import Own_Material
from designClass.design import Design


class Material_Creater(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Creater, self).__init__(**kwargs)
        self.cols=2
        self.btnSize=Design.btnSize
        self.createGui()
        self._parent=None
        self.focus_btn=None
    
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def createGui(self):
        self.createPopups()
        self.createButtons()
        self.add_widget(Label(text='name: '))
        self.add_widget(self.name_btn)
        self.add_widget(Label(text='price[euro/kg]:'))
        self.add_widget(self.price_btn)
        self.add_widget(Label(text='density[kg/m^3]:'))
        self.add_widget(self.density_btn)
        self.add_widget(Label(text='stiffness[MPa]:'))
        self.add_widget(self.stiffness_btn)
        self.add_widget(Label(text='strength[MPa]:'))
        self.add_widget(self.strength_btn)
        self.add_widget(self.cancel_btn)
        self.add_widget(self.create_btn)
    
    '''
    the method createButtons create all buttons of the class
    '''
    def createButtons(self):
        #materialname
        self.name_btn=Button(text='name',size_hint_y=None, height=self.btnSize)
        self.name_btn.bind(on_press=self.useKeyboard)
        #materialprice
        self.price_btn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.price_btn.bind(on_press=self.useNumpad)
        #materialdensity
        self.density_btn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.density_btn.bind(on_press=self.useNumpad)
        #materialstiffness
        self.stiffness_btn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.stiffness_btn.bind(on_press=self.useNumpad)
        #materialstrength
        self.strength_btn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.strength_btn.bind(on_press=self.useNumpad)
        #create material and cancel 
        self.create_btn=Button(text='create',size_hint_y=None, height=self.btnSize)
        self.create_btn.bind(on_press=self.createMaterial)
        self.cancel_btn=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        self.cancel_btn.bind(on_press=self.cancel)
        
    '''
    the method use_keyword open the keyboard_popup for the user
    '''
    def useKeyboard(self,button):
        self.keyboard.textinput.text=button.text
        self.popup_keyboard.open()
    
    '''
    the method useNumpad open the numpad_popup for the user
    '''
    def useNumpad(self,button):
        self.focus_btn=button
        self.numpad.textinput.text=button.text
        self.popup_numpad.open()
        
    '''
    the method createPopups create the popups 
    and sign in by the keyboard and numpad 
    '''
    def createPopups(self):
        self.numpad=Numpad()
        self.keyboard=Keyboard()
        self.popup_keyboard=Popup(title='name:',content=self.keyboard)
        self.popup_numpad=Popup(title='numpad', content=self.numpad)
        self.numpad.signInParent(self)
        self.keyboard.signInParent(self)
    
    
    '''
    the method finishedKeyboard close the keyboard_popup
    '''
    def finishedKeyboard(self):
        self.name_btn.text=self.keyboard.textinput.text
        self.popup_keyboard.dismiss()
        self.keyboard.resetText()
    
    '''
    the method finishedNumpad close the numpad_popup
    '''
    def finishedNumpad(self):
        self.focus_btn.text=self.numpad.textinput.text
        self.popup_numpad.dismiss()
        self.numpad.resetText()
    
    '''
    the method signInParent to set the parent of 
    the object. the parent must have the method update_materials
    '''
    def signInParent(self, parent):
        self._parent=parent
    
    '''
    the method resetEditor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''
    def resetEditor(self):
        self.name_btn.text='name'
        self.price_btn.text='0.0'
        self.density_btn.text='0.0'
        self.stiffness_btn.text='0.0'
        self.strength_btn.text='0.0'
    
    '''
    the method create material create a own_material and update the 
    materiallist all_materials and the layout where you can choose 
    the materials
    '''
    def createMaterial(self,button):
        cur_material=Own_Material(self.name_btn.text,self.price_btn.text,self.density_btn.text,self.stiffness_btn.text,self.strength_btn.text)
        self._parent.all_materials.addMaterial(cur_material)
        self._parent.cancelEditMaterial()
    
    '''
    cancel the create-process
    '''
    def cancel(self,button):
        self._parent.cancelEditMaterial()
