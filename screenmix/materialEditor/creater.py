'''
Created on 04.04.2016
@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from materials.ownMaterial import OwnMaterial
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class MaterialCreater(GridLayout):
    
    '''
    the material-creater is the component, where the user 
    can add new material
    '''
    
    # important components
    p = ObjectProperty()  # parent
    
    # strings
    createStr, cancelStr = StringProperty('create'), StringProperty('cancel')
    # properties of the material
    densityStr, stiffnessStr = StringProperty('density[kg/m^3]:'), StringProperty('stiffness[MPa]:')
    priceStr, strengthStr = StringProperty('price[euro/kg]:'), StringProperty('strength[MPa]:')
    nameStr, defaultValueStr = StringProperty('name'), StringProperty('1.0')
    
    
    
    # constructor
    def __init__(self, **kwargs):
        super(MaterialCreater, self).__init__(**kwargs)
        self.cols, self.spacing = 2, Design.spacing
        self.height = Design.btnHeight
        self.create_gui()
    
    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''
    def create_gui(self):
        self.create_popups()
        self.create_buttons()
        self.add_widget(OwnLabel(text=self.nameStr))
        self.add_widget(self.btnName)
        self.add_widget(OwnLabel(text=self.priceStr))
        self.add_widget(self.btnPrice)
        self.add_widget(OwnLabel(text=self.densityStr))
        self.add_widget(self.btnDensity)
        self.add_widget(OwnLabel(text=self.stiffnessStr))
        self.add_widget(self.btnStiffness)
        self.add_widget(OwnLabel(text=self.strengthStr))
        self.add_widget(self.btnStrength)
        self.add_widget(self.btnCancel)
        self.add_widget(self.btnCreate)
    
    '''
    the method create_buttons create all buttons of the class
    '''
    def create_buttons(self):
        # materialname
        self.btnName = OwnButton(text=self.nameStr)
        self.btnName.bind(on_press=self.use_keyboard)
        # materialprice
        self.btnPrice = OwnButton(text=self.defaultValueStr)
        self.btnPrice.bind(on_press=self.use_numpad)
        # materialdensity
        self.btnDensity = OwnButton(text=self.defaultValueStr)
        self.btnDensity.bind(on_press=self.use_numpad)
        # materialstiffness
        self.btnStiffness = OwnButton(text=self.defaultValueStr)
        self.btnStiffness.bind(on_press=self.use_numpad)
        # materialstrength
        self.btnStrength = OwnButton(text=self.defaultValueStr)
        self.btnStrength.bind(on_press=self.use_numpad)
        # create material and cancel 
        self.btnCreate = OwnButton(text=self.createStr)
        self.btnCreate.bind(on_press=self.create_material)
        self.btnCancel = OwnButton(text=self.cancelStr)
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
        # find the property and set the title of the popup
        if self.btnFocus == self.btnDensity:
            self.popupNumpad.title = self.densityStr
        elif self.btnFocus == self.btnPrice:
            self.popupNumpad.title = self.priceStr
        elif self.btnFocus == self.btnStiffness:
            self.popupNumpad.title = self.stiffnessStr
        elif self.btnFocus == self.btnStrength:
            self.popupNumpad.title = self.strengthStr
        self.popupNumpad.open()
        
    '''
    the method create_popups create the popups 
    and sign in by the keyboard and numpad 
    '''
    def create_popups(self):
        self.numpad = Numpad(p=self)
        self.keyboard = Keyboard()
        self.popupKeyboard = OwnPopup(title=self.nameStr, content=self.keyboard)
        self.popupNumpad = OwnPopup(content=self.numpad)
        self.keyboard.p = self
    
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
    the method reset_editor reset the values of the editor
    the method must be called, when the user cancel or add 
    the material
    '''
    def reset_editor(self):
        self.btnName.text = self.nameStr
        self.btnPrice.text = self.defaultValueStr
        self.btnDensity.text = self.defaultValueStr
        self.btnStiffness.text = self.defaultValueStr
        self.btnStrength.text = self.defaultValueStr
    
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
    def close_numpad(self):
        self.popupNumpad.dismiss()
    
    '''
    cancel the create-process
    '''
    def cancel_creating(self, btn):
        self.p.cancel_edit_material()
