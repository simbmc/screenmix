'''
Created on 11.04.2016
@author: mkennert
'''
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from materialEditor.creater import MaterialCreater
from ownComponents.design import Design
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
            btn.bind(on_press=self.show_material_information)
            self.materialLayout.add_widget(btn)
        self.btnMaterialEditor = OwnButton(text='create material')
        self.btnMaterialEditor.bind(on_press=self.create_material)
        self.materialLayout.add_widget(self.btnMaterialEditor)
        self.add_widget(self.materialLayout)

    '''
    popupInfo to show the material information
    popupCreate to create new material
    '''

    def create_popups(self):
        creater = MaterialCreater()
        creater.p = self
        self.popupInfo = OwnPopup(title='material', content=self.contentLayout)
        self.popupCreate = OwnPopup(title='create new material', content=creater)

    '''
    create the gui which is necessary for the show of the 
    material-information
    '''

    def create_material_information(self):
        self.lblName, self.lblPrice = OwnLabel(), OwnLabel()
        self.lblDensity, self.lblStiffness = OwnLabel(), OwnLabel()
        self.lblStrenght = OwnLabel()
        self.contentLayout = GridLayout(cols=2)
        self.contentLayout.add_widget(OwnLabel(text='name:'))
        self.contentLayout.add_widget(self.lblName)
        self.contentLayout.add_widget(OwnLabel(text='price[euro/kg]:'))
        self.contentLayout.add_widget(self.lblPrice)
        self.contentLayout.add_widget(OwnLabel(text='density[kg/m^3]:'))
        self.contentLayout.add_widget(self.lblDensity)
        self.contentLayout.add_widget(OwnLabel(text='stiffness[MPa]:'))
        self.contentLayout.add_widget(self.lblStiffness)
        self.contentLayout.add_widget(OwnLabel(text='strength[MPa]:'))
        self.contentLayout.add_widget(self.lblStrenght)
        btn_back = OwnButton(text='back')
        btn_back.bind(on_press=self.cancel_show)
        self.contentLayout.add_widget(btn_back)
        self.create_popups()

    '''
    set the labeltext with the materialproperties
    '''

    def show_material_information(self, button):
        for i in range(0, self.cs.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == button.text:
                name=self.allMaterials.allMaterials[i].name
                self.lblName.text = name
                self.lblPrice.text = str(self.allMaterials.allMaterials[i].price)
                self.lblDensity.text = str(self.allMaterials.allMaterials[i].density)
                self.lblStiffness.text = str(self.allMaterials.allMaterials[i].stiffness)
                self.lblStrenght.text = str(self.allMaterials.allMaterials[i].strength)
                self.popupInfo.title=name
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
