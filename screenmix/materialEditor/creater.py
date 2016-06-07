'''
Created on 04.04.2016
@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from materialEditor.keyboard import Keyboard
from materialEditor.numpad import Numpad
from materials.ownMaterial import OwnMaterial
from designClass.design import Design


class MaterialCreater(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        self.cols=2
        self.btnSize=Design.btnSize
        self.create_gui()
        self.p=None
        self.focusBtn=None
    
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_popups()
        self.create_buttons()
        self.add_widget(Label(text='name: '))
        self.add_widget(self.nameBtn)
        self.add_widget(Label(text='price[euro/kg]:'))
        self.add_widget(self.priceBtn)
        self.add_widget(Label(text='density[kg/m^3]:'))
        self.add_widget(self.densityBtn)
        self.add_widget(Label(text='stiffness[MPa]:'))
        self.add_widget(self.stiffnessBtn)
        self.add_widget(Label(text='strength[MPa]:'))
        self.add_widget(self.strengthBtn)
        self.add_widget(self.cancelBtn)
        self.add_widget(self.createBtn)
    
    '''
    the method create_buttons create all buttons of the class
    '''
    def create_buttons(self):
        #materialname
        self.nameBtn=Button(text='name',size_hint_y=None, height=self.btnSize)
        self.nameBtn.bind(on_press=self.use_keyboard)
        #materialprice
        self.priceBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.priceBtn.bind(on_press=self.use_numpad)
        #materialdensity
        self.densityBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.densityBtn.bind(on_press=self.use_numpad)
        #materialstiffness
        self.stiffnessBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.stiffnessBtn.bind(on_press=self.use_numpad)
        #materialstrength
        self.strengthBtn=Button(text='1.0',size_hint_y=None, height=self.btnSize)
        self.strengthBtn.bind(on_press=self.use_numpad)
        #create material and cancel 
        self.createBtn=Button(text='create',size_hint_y=None, height=self.btnSize)
        self.createBtn.bind(on_press=self.create_material)
        self.cancelBtn=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        self.cancelBtn.bind(on_press=self.cancel)
        
    '''
    the method use_keyword open the keyboard_popup for the user
    '''
    def use_keyboard(self,button):
        self.keyboard.textinput.text=button.text
        self.popupKeyboard.open()
    
    '''
    the method use_numpad open the numpad_popup for the user
    '''
    def use_numpad(self,btn):
        self.focusBtn=btn
        self.numpad.textinput.text=btn.text
        self.popupNumpad.open()
        
    '''
    the method create_popups create the popups 
    and sign in by the keyboard and numpad 
    '''
    def create_popups(self):
        self.numpad=Numpad()
        self.keyboard=Keyboard()
        self.popupKeyboard=Popup(title='name:',content=self.keyboard)
        self.popupNumpad=Popup(title='numpad', content=self.numpad)
        self.numpad.sign_in_parent(self)
        self.keyboard.sign_in_parent(self)
    
    
    '''
    the method finished_keyboard close the keyboard_popup
    '''
    def finished_keyboard(self):
        self.nameBtn.text=self.keyboard.textinput.text
        self.popupKeyboard.dismiss()
        self.keyboard.reset_text()
    
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
    
    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method update_materials
    '''
    def sign_in_parent(self, parent):
        self.p=parent
    
    '''
    the method reset_editor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''
    def reset_editor(self):
        self.nameBtn.text='name'
        self.priceBtn.text='0.0'
        self.densityBtn.text='0.0'
        self.stiffnessBtn.text='0.0'
        self.strengthBtn.text='0.0'
    
    '''
    the method create material create a own_material and update the 
    materiallist allMaterials and the layout where you can choose 
    the materials
    '''
    def create_material(self,button):
        cur_material=OwnMaterial(self.nameBtn.text,self.priceBtn.text,self.densityBtn.text,self.stiffnessBtn.text,self.strengthBtn.text)
        self.p.allMaterials.add_Material(cur_material)
        self.p.cancel_edit_material()
    
    '''
    cancel the create-process
    '''
    def cancel(self,button):
        self.p.cancel_edit_material()