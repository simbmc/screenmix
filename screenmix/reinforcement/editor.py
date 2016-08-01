'''
Created on 02.06.2016

@author: mkennert

'''
from decimal import Decimal

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from reinforcement.shapeSelection import ShapeSelection


class ReinforcementEditor(GridLayout, IObserver):
    cs = ObjectProperty()
    #constructor

    def __init__(self, **kwargs):
        super(ReinforcementEditor, self).__init__(**kwargs)
        self.cols = 1
        self.spacing=2
        self.padding=[10,10,10,10]
        self.btnSize = Design.btnHeight
        self.containsInformation = False
        self.error = False
        
    '''
    create the gui
    '''

    def create_gui(self):
        #if you add more shapes, uncomment the follow row
        self.create_selection_menu()
        self.create_cross_section_area()
        self.create_add_delete_area()
        self.create_material_information()
        self.create_add_layer_information_area()

    '''
    the method create_add_delete_area create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete_area(self):
        self.addDeleteLayout = GridLayout(cols=2, row_force_default=True,
                                    row_default_height=Design.btnHeight,
                                    size_hint_y=None, height=Design.btnHeight,
                                    spacing=2)
        btnAdd = OwnButton(text='add layer')
        btnDelete = OwnButton(text='delete layer')
        btnAdd.bind(on_press=self.show_add_layer_area)
        btnDelete.bind(on_press=self.delete_layer)
        self.addDeleteLayout.add_widget(btnAdd)
        self.addDeleteLayout.add_widget(btnDelete)
        self.add_widget(self.addDeleteLayout)

    '''
    the method create_material_information create the area where you can 
    see the information about the selected materials
    '''

    def create_material_information(self):
        self.materialLayout = GridLayout(cols=1)
        self.lblName, self.lblPrice = OwnLabel(text='-'), OwnLabel(text='-')
        self.lblDensity, self.lblStiffness = OwnLabel(text='-'), OwnLabel(text='-')
        self.lblStrength, self.lblPercent = OwnLabel(text='-'), OwnLabel(text='10 %')
        materialLayout = GridLayout(cols=4, row_force_default=True, 
                                    row_default_height=2 * Design.lblHeight,
                                    height=self.btnSize)
        materialLayout.add_widget(OwnLabel(text='name:'))
        materialLayout.add_widget(self.lblName)
        materialLayout.add_widget(OwnLabel(text='price:'))
        materialLayout.add_widget(self.lblPrice)
        materialLayout.add_widget(OwnLabel(text='density:'))
        materialLayout.add_widget(self.lblDensity)
        materialLayout.add_widget(OwnLabel(text='stiffness:'))
        materialLayout.add_widget(self.lblStiffness)
        materialLayout.add_widget(OwnLabel(text='tensile strength:'))
        materialLayout.add_widget(self.lblStrength)
        materialLayout.add_widget(OwnLabel(text='percent:'))
        materialLayout.add_widget(self.lblPercent)
        self.slidePercent = Slider(min=0.05, max=0.2, value=0.1)
        self.slidePercent.bind(value=self.set_percent)
        self.materialLayout.add_widget(materialLayout)
        self.materialLayout.add_widget(self.slidePercent)
        self.add_widget(self.materialLayout)

    '''
    the method create_cross_section_area create the area where you can 
    see the information of the cs_view
    '''

    def create_cross_section_area(self):
        self.lblcsPrice = OwnLabel(text='-')
        self.lblcsWeight = OwnLabel(text='-')
        self.lblcsStrength = OwnLabel(text='-')
        self.csLayout = GridLayout(cols=2, row_force_default=True, 
                                   row_default_height=3 * Design.lblHeight,
                                   height=3 * Design.lblHeight)
        self.csLayout.add_widget(OwnLabel(text='price [Euro/m]:'))
        self.csLayout.add_widget(self.lblcsPrice)
        self.csLayout.add_widget(OwnLabel(text='weight [kg]:'))
        self.csLayout.add_widget(self.lblcsWeight)
        self.csLayout.add_widget(OwnLabel(text='tensile strength [MPa]:'))
        self.csLayout.add_widget(self.lblcsStrength)
        self.add_widget(self.csLayout)

    '''
    the method create_add_layer_information_area create the area where you can 
    add new materials
    '''

    def create_add_layer_information_area(self):
        self.create_material_options()
        btnConfirm = OwnButton(text='confirm')
        btnConfirm.bind(on_press=self.add_layer)
        btnCancel = OwnButton(text='cancel')
        btnCancel.bind(on_press=self.cancel_adding)
        self.addLayout = GridLayout(cols=2, spacing=2,row_force_default=True, 
                                    row_default_height=Design.btnHeight,
                                    height=self.btnSize)
        self.addLayout.add_widget(OwnLabel(text='material:'))
        self.btnMaterialOption = OwnButton(text='steel')
        self.btnMaterialOption.bind(on_release=self.popup.open)
        self.addLayout.add_widget(self.btnMaterialOption)
        self.lblMaterialPercent = OwnLabel(text='percent: 10%')
        self.addLayout.add_widget(self.lblMaterialPercent)
        self.sliderLayerPercent = Slider(min=0.05, max=0.2, value=0.1)
        self.sliderLayerPercent.bind(value=self.set_percenet_while_creating)
        self.addLayout.add_widget(self.sliderLayerPercent)
        self.addLayout.add_widget(btnConfirm)
        self.addLayout.add_widget(btnCancel)
        

    '''
    the method create_material_options create the popup where you can 
    select the materials for the new layer
    '''

    def create_material_options(self):
        self.materialSelectionLayout = GridLayout(
            cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.materialSelectionLayout .bind(
            minimum_height=self.materialSelectionLayout.setter('height'))
        self.materialEditor = MaterialCreater()
        self.materialEditor.sign_in_parent(self)
        self.popupMaterialEditor = OwnPopup(
            title='editor', content=self.materialEditor)
        for i in range(0, self.allMaterials.get_length()):
            btnMaterialA = OwnButton(text=self.allMaterials.allMaterials[i].name)
            btnMaterialA.bind(on_press=self.select_material)
            self.materialSelectionLayout.add_widget(btnMaterialA)
        self.btnMaterialEditor = OwnButton(text='create material')
        self.btnMaterialEditor.bind(on_press=self.popupMaterialEditor.open)
        self.materialSelectionLayout.add_widget(self.btnMaterialEditor)
        self.root = ScrollView()
        self.root.add_widget(self.materialSelectionLayout)
        self.popup = OwnPopup(title='materials', content=self.root)
    
    '''
    create the layout where you can select the cross-section-shape
    '''

    def create_selection_menu(self):
        self.create_popup_shape()
        selectionContent = GridLayout(cols=2,
                                      size_hint_y=None, row_force_default=True,
                                      row_default_height=Design.btnHeight,
                                      height=Design.btnHeight)
        self.btnSelection = OwnButton(text='rectangle')
        self.btnSelection.bind(on_press=self.show_shape_selection)
        selectionContent.add_widget(OwnLabel(text='shape'))
        selectionContent.add_widget(self.btnSelection)
        self.add_widget(selectionContent)
    
    '''
    create popup where you can select the shape of the cross section
    '''

    def create_popup_shape(self):
        shapeContent = ShapeSelection()
        shapeContent.set_information(self)
        self.shapeSelection = OwnPopup(title='shape', content=shapeContent)
    
    '''
    open the popup where the user can select the shape
    '''

    def show_shape_selection(self, btn):
        self.shapeSelection.open()
    
    '''
    look which shape the user has selected
    '''

    def finished_shape_selection(self, btn):
        if btn.text == 'rectangle':
            self.btnSelection.text=btn.text
            self.cs.show_rectangle()
        self.shapeSelection.dismiss()
    
    '''
    cancel the shape-selection
    '''
    def cancel_shape_selection(self):
        self.shapeSelection.dismiss()
        
    '''
    add the information of the selected shape
    '''
    def show_information(self, information):
        if not self.containsInformation:
            self.information = information
            self.add_widget(self.information, 3)
        else:
            self.remove_widget(self.information)
            self.information = information
            self.add_widget(self.information, 3)

    '''
    the method show_add_layer_area was developed to show the 
    the addLayout and hide the material_information
    '''

    def show_add_layer_area(self, button):
        self.remove_widget(self.materialLayout)
        self.remove_widget(self.addDeleteLayout)
        self.sliderLayerPercent.value = 0.1
        self.add_widget(self.addLayout, 0)

    '''
    the method finished_adding was developed to hide the 
    the addLayout and show the materialLayout
    '''

    def finished_adding(self):
        self.remove_widget(self.addLayout)
        self.add_widget(self.materialLayout, 0)
        self.add_widget(self.addDeleteLayout, 1)

    '''
    the method add_layer add a new layer at the cross section
    it use the choosen slidePercent value
    '''

    def add_layer(self, button):
        self.finished_adding()
        for i in range(0, self.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == self.btnMaterialOption.text:
                self.cs.add_layer(
                    self.sliderLayerPercent.value, self.allMaterials.allMaterials[i])
                return

    '''
    the method cancel_adding would be must call when the user wouldn't 
    add a new materials
    '''

    def cancel_adding(self, button):
        self.finished_adding()

    '''
    the method delete_layer was developed to delete a existing
    materials
    '''

    def delete_layer(self, button):
        self.cs.delete_layer()

    '''
    the method update_layer_information was developed to update
    the information, when the user selected a other rectangle in the view
    '''

    def update_layer_information(self, name, price, density, stiffness, strength, percent):
        self.lblName.text, self.lblPrice.text = str(name), str(price)
        self.lblDensity.text = str(density)
        self.lblStiffness.text = str(stiffness)
        self.lblStrength.text = str(strength)
        self.lblPercent.text=str(int(percent*100))+' %'
        self.slidePercent.value = percent


    '''
    the method update_cs_information update the cross section information.
    '''

    def update_cs_information(self, price, weight, strength):
        self.lblcsPrice.text = '%.2E' % Decimal(str(price))
        self.lblcsWeight.text = '%.2E' % Decimal(str(weight))
        self.lblcsStrength.text = '%.2E' % Decimal(str(strength))

    '''
    the method cancel_edit_material cancel the editing of the material
    and reset the values of the materialEditor
    '''

    def cancel_edit_material(self):
        self.popupMaterialEditor.dismiss()
        self.materialEditor.reset_editor()

    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''

    def update(self):
        self.materialSelectionLayout.remove_widget(self.btnMaterialEditor)
        btnMaterial = OwnButton(text=self.allMaterials.allMaterials[-1].name)
        btnMaterial.bind(on_press=self.select_material)
        self.materialSelectionLayout.add_widget(btnMaterial)
        self.materialSelectionLayout.add_widget(self.btnMaterialEditor)

    '''
    the method will be called when the user selected a material
    the popup will be closed and the button text change to the material
    lblName
    '''

    def select_material(self, btn):
        self.popup.dismiss()
        self.btnMaterialOption.text = btn.text

    '''
    the method set_percenet_while_creating change the percentage share 
    of the materials. Attention: this method must be call 
    when the materials isn't exist
    '''

    def set_percenet_while_creating(self, inst, value):
        self.lblMaterialPercent.text = 'percent: ' + \
            str(int(value * 100)) + ' %'

    '''
    set the percentage share of the layer which has the focus
    '''

    def set_percent(self, instance, value):
        self.sliderLayerPercent.value = value
        self.cs.view.set_percent(value)
        value=int(value*100)
        self.lblPercent.text=str(value)+' %'

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.allMaterials = self.cs.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
