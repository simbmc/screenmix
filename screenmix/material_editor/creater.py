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


class Material_Creater(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Material_Creater, self).__init__(**kwargs)
        self.cols=2
        self.create_gui()
        self._parent=None
        self.focus_btn=None
    
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_popups()
        self.create_buttons()
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
    the method create_buttons create all buttons of the class
    '''
    def create_buttons(self):
        #materialname
        self.name_btn=Button(text='name')
        self.name_btn.bind(on_press=self.use_keyboard)
        #materialprice
        self.price_btn=Button(text='0.0')
        self.price_btn.bind(on_press=self.use_numpad)
        #materialdensity
        self.density_btn=Button(text='0.0')
        self.density_btn.bind(on_press=self.use_numpad)
        #materialstiffness
        self.stiffness_btn=Button(text='0.0')
        self.stiffness_btn.bind(on_press=self.use_numpad)
        #materialstrength
        self.strength_btn=Button(text='0.0')
        self.strength_btn.bind(on_press=self.use_numpad)
        #create material and cancel 
        self.create_btn=Button(text='create')
        self.create_btn.bind(on_press=self.create_material)
        self.cancel_btn=Button(text='cancel')
        self.cancel_btn.bind(on_press=self.cancel)
        
    '''
    the method use_keyword open the keyboard_popup for the user
    '''
    def use_keyboard(self,button):
        self.keyboard.textinput.text=button.text
        self.popup_keyboard.open()
    
    '''
    the method use_numpad open the numpad_popup for the user
    '''
    def use_numpad(self,button):
        self.focus_btn=button
        self.numpad.textinput.text=button.text
        self.popup_numpad.open()
        
    '''
    the method create_popups create the popups 
    and sign in by the keyboard and numpad 
    '''
    def create_popups(self):
        self.numpad=Numpad()
        self.keyboard=Keyboard()
        self.popup_keyboard=Popup(title='name:',content=self.keyboard)
        self.popup_numpad=Popup(title='numpad', content=self.numpad)
        self.numpad.sign_in_parent(self)
        self.keyboard.sign_in_parent(self)
    
    
    '''
    the method finished_keyboard close the keyboard_popup
    '''
    def finished_keyboard(self):
        self.name_btn.text=self.keyboard.textinput.text
        self.popup_keyboard.dismiss()
        self.keyboard.reset_text()
    
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focus_btn.text=self.numpad.textinput.text
        self.popup_numpad.dismiss()
        self.numpad.reset_text()
    
    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method update_materials
    '''
    def sign_in_parent(self, parent):
        self._parent=parent
    
    '''
    the method reset_editor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''
    def reset_editor(self):
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
    def create_material(self,button):
        cur_material=Own_Material(self.name_btn.text,self.price_btn.text,self.density_btn.text,self.stiffness_btn.text,self.strength_btn.text)
        self._parent.all_materials.add_Material(cur_material)
        self._parent.cancel_edit_material()
    
    '''
    cancel the create-process
    '''
    def cancel(self,button):
        self._parent.cancel_edit_material()
