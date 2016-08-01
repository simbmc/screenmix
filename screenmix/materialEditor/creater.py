'''
Created on 04.04.2016
@author: mkennert
'''
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from materials.ownMaterial import OwnMaterial
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class MaterialCreater(GridLayout):
    #p=parent
    p = ObjectProperty()
    #constructor
    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        self.cols = 2
        self.btnHeight = Design.btnHeight
        self.spacing = 5
        self.btnFocus, self.p = None, None
        self.create_gui()
    
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_popups()
        self.create_buttons()
        self.add_widget(OwnLabel(text='name: '))
        self.add_widget(self.btnName)
        self.add_widget(OwnLabel(text='price[euro/kg]:'))
        self.add_widget(self.btnPrice)
        self.add_widget(OwnLabel(text='density[kg/m^3]:'))
        self.add_widget(self.btnDensity)
        self.add_widget(OwnLabel(text='stiffness[MPa]:'))
        self.add_widget(self.btnStiffness)
        self.add_widget(OwnLabel(text='strength[MPa]:'))
        self.add_widget(self.btnStrength)
        self.add_widget(self.btnCancel)
        self.add_widget(self.btnCreate)
    
    '''
    the method create_buttons create all buttons of the class
    '''
    def create_buttons(self):
        # materialname
        self.btnName = OwnButton(text='name')
        self.btnName.bind(on_press=self.use_keyboard)
        # materialprice
        self.btnPrice = OwnButton(text='1.0')
        self.btnPrice.bind(on_press=self.use_numpad)
        # materialdensity
        self.btnDensity = OwnButton(text='1.0')
        self.btnDensity.bind(on_press=self.use_numpad)
        # materialstiffness
        self.btnStiffness = OwnButton(text='1.0')
        self.btnStiffness.bind(on_press=self.use_numpad)
        # materialstrength
        self.btnStrength = OwnButton(text='1.0')
        self.btnStrength.bind(on_press=self.use_numpad)
        # create material and cancel 
        self.btnCreate = OwnButton(text='create')
        self.btnCreate.bind(on_press=self.create_material)
        self.btnCancel = OwnButton(text='cancel')
        self.btnCancel.bind(on_press=self.cancel_creating)
        
    '''
    the method use_keyword open the keyboard_popup for the user
    '''
    def use_keyboard(self, button):
        self.keyboard.lblTextinput.text = button.text
        self.popupKeyboard.open()
    
    '''
    the method use_numpad open the numpad_popup for the user
    '''
    def use_numpad(self, btn):
        self.btnFocus = btn
        self.numpad.lblTextinput.text = btn.text
        self.popupNumpad.open()
        
    '''
    the method create_popups create the popups 
    and sign in by the keyboard and numpad 
    '''
    def create_popups(self):
        self.numpad = Numpad()
        self.keyboard = Keyboard()
        self.popupKeyboard = OwnPopup(title='name:', content=self.keyboard)
        self.popupNumpad = OwnPopup(title='numpad', content=self.numpad)
        self.numpad.sign_in_parent(self)
        self.keyboard.sign_in_parent(self)
    
    
    '''
    the method finished_keyboard close the keyboard_popup
    '''
    def finished_keyboard(self):
        self.btnName.text = self.keyboard.lblTextinput.text
        self.popupKeyboard.dismiss()
        self.keyboard.reset_text()
    
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.btnFocus.text = self.numpad.lblTextinput.text
        self.popupNumpad.dismiss()
        self.numpad.reset_text()
    
    '''
    the method sign_in_parent to set the parent of 
    the object. the parent must have the method update_materials
    '''
    def sign_in_parent(self, parent):
        self.p = parent
    
    '''
    the method reset_editor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''
    def reset_editor(self):
        self.btnName.text = 'name'
        self.btnPrice.text = '1.0'
        self.btnDensity.text = '1.0'
        self.btnStiffness.text = '1.0'
        self.btnStrength.text = '1.0'
    
    '''
    the method create material create a own_material and update the 
    materiallist allMaterials and the layout where you can choose 
    the materials
    '''
    def create_material(self, button):
        material = OwnMaterial(self.btnName.text, self.btnPrice.text,
                             self.btnDensity.text, self.btnStiffness.text,
                             self.btnStrength.text)
        self.p.allMaterials.add_material(material)
        self.p.cancel_edit_material()
    
    '''
    close the numpad
    '''
    def closeNumpad(self):
        self.popupNumpad.dismiss()
    
    '''
    cancel the create-process
    '''
    def cancel_creating(self, btn):
        self.p.cancel_edit_material()
