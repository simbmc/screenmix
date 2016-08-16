'''
Created on 11.04.2016
@author: mkennert
'''
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from materialEditor.creater import MaterialCreater
from ownComponents.design import Design
from ownComponents.keyboard import Keyboard
from ownComponents.numpad import Numpad
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup


class Material_Editor(ScrollView):
    
    '''
    the material-edit is the component, where the user 
    can see the materials and create new material with 
    the material-creater
    '''
    
    #important components
    cs = ObjectProperty()
    
    #constructor
    def __init__(self, **kwargs):
        super(Material_Editor, self).__init__(**kwargs)

    '''
    the method create gui create the gui of 
    the material_editor and create the popups
    '''

    def create_gui(self):
        self.create_material_information()
        self.materialLayout = GridLayout(cols=1, spacing=Design.spacing, size_hint_y=None)
        self.materialLayout.padding = Design.padding
        # Make sure the height is such that there is something to scroll.
        self.materialLayout.bind(minimum_height=self.materialLayout.setter('height'))
        for i in self.allMaterials.allMaterials:
            btn = OwnButton(text=i.name)
            btn.height=dp(55)
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor = OwnButton(text='create material')
        self.btnMaterialEditor.height=dp(55)
        self.btnMaterialEditor.bind(on_press=self.create_material)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.materialLayout)
        

    '''
    popupInfo to show the material information
    popupCreate to create new material
    '''

    def create_popups(self):
        self.numpad,self.keyboard=Numpad(),Keyboard()
        self.numpad.p,self.keyboard.p=self,self
        self.editNumpad=OwnPopup(content=self.numpad)
        self.editKeyboard=OwnPopup(content=self.keyboard)
        creater = MaterialCreater()
        creater.p = self
        self.popupInfo = OwnPopup(title='material', content=self.contentLayout)
        self.popupCreate = OwnPopup(title='create new material', content=creater)

    '''
    create the gui which is necessary for the show of the 
    material-information
    '''

    def create_material_information(self):
        #create the btns to edit the values or the name
        self.btnName, self.btnPrice = OwnButton(), OwnButton()
        self.btnDensity, self.btnStiffness = OwnButton(), OwnButton()
        self.btnStrenght = OwnButton()
        #bind the values to the methods show_numpad and show_keyboard
        self.btnName.bind(on_press=self.show_keyboard)
        self.btnPrice.bind(on_press=self.show_numpad)
        self.btnDensity.bind(on_press=self.show_numpad)
        self.btnStiffness.bind(on_press=self.show_numpad)
        self.btnStrenght.bind(on_press=self.show_numpad)
        #fill the contentLayout with the components
        self.contentLayout = GridLayout(cols=2,spacing=Design.spacing)
        self.contentLayout.add_widget(OwnLabel(text='name:'))
        self.contentLayout.add_widget(self.btnName)
        self.contentLayout.add_widget(OwnLabel(text='price[euro/kg]:'))
        self.contentLayout.add_widget(self.btnPrice)
        self.contentLayout.add_widget(OwnLabel(text='density[kg/m^3]:'))
        self.contentLayout.add_widget(self.btnDensity)
        self.contentLayout.add_widget(OwnLabel(text='stiffness[MPa]:'))
        self.contentLayout.add_widget(self.btnStiffness)
        self.contentLayout.add_widget(OwnLabel(text='strength[MPa]:'))
        self.contentLayout.add_widget(self.btnStrenght)
        #btn_back=go back to the materials-view
        btn_back = OwnButton(text='back')
        btn_back.bind(on_press=self.cancel_show)
        #edit the new values
        btn_confirm=OwnButton(text='confirm')
        btn_confirm.bind(on_press=self.edit_material)
        self.contentLayout.add_widget(btn_back)
        self.contentLayout.add_widget(btn_confirm)
        self.create_popups()

    '''
    set the labeltext with the materialproperties
    '''

    def show_material_information(self, button):
        for i in range(0, self.cs.allMaterials.get_length()):
            material=self.allMaterials.allMaterials[i]
            if material.name == button.text:
                self.focusMaterial=material
                self.btnName.text = material.name
                self.btnPrice.text = str(material.price)
                self.btnDensity.text = str(material.density)
                self.btnStiffness.text = str(material.stiffness)
                self.btnStrenght.text = str(material.strength)
                self.popupInfo.title=material.name
                self.popupInfo.open()

    '''
    close the popup, which shows the information from
    the choosen material
    '''

    def cancel_show(self, button):
        self.popupInfo.dismiss()

    '''
    open the popup, which has the creator as contentLayout
    '''

    def create_material(self, button):
        self.popupCreate.open()

    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.materialLayout.remove_widget(self.btnMaterialEditor)
        btn_material_A = OwnButton(
            text=self.allMaterials.allMaterials[-1].name)
        btn_material_A.bind(on_press=self.show_material_information)
        self.materialLayout.add_widget(btn_material_A)
        self.materialLayout.add_widget(self.btnMaterialEditor)

    '''
    cancel the create-process. this method 
    is necessary, because editor is the parent 
    of the creator and creator call the method cancel_edit_material
    from the parent
    '''

    def cancel_edit_material(self):
        self.popupCreate.dismiss()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.allMaterials = self.cs.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
    
    '''
    edit the selected material by the new values
    '''
    def edit_material(self,btn):
        self.popupInfo.dismiss()
        self.focusMaterial.name=self.btnName.text
        self.focusMaterial.density=float(self.btnDensity.text)
        self.focusMaterial.price=float(self.btnPrice.text)
        self.focusMaterial.stiffness=float(self.btnStiffness.text)
        self.focusMaterial.strength=float(self.btnStrenght.text)
        if self.focusMaterial.name=='concrete':
            self.cs.update_concrete_information(self.focusMaterial.density,self.focusMaterial.price,
                                                self.focusMaterial.stiffness,self.focusMaterial.strength)
        self.cs.update_informations()
    
    '''
    open the popup to edit the value of the material
    '''
    def show_numpad(self,btn):
        self.focusBtn=btn
        self.numpad.lblTextinput.text=btn.text
        self.editNumpad.open()
    
    '''
    open the popup to edit the name of the material
    '''
    def show_keyboard(self,btn):
        self.focusBtn=btn
        self.keyboard.lblTextinput.text=btn.text
        self.editKeyboard.open()
    
    '''
    finished the name-input and the set the text of the 
    btnName
    '''
    def finished_keyboard(self):
        self.focusBtn.text=self.keyboard.lblTextinput.text
        self.editKeyboard.dismiss()
    
    '''
    finished the value-input and set the text of the focusbtn
    to the value
    '''
    def finished_numpad(self):
        self.focusBtn.text=self.numpad.lblTextinput.text
        self.editNumpad.dismiss()
    
    '''
    close the numpad and change nothing
    '''
    def closeNumpad(self):
        self.editNumpad.dismiss()
    