'''
Created on 02.06.2016

@author: mkennert

'''
from decimal import Decimal

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from materialEditor.creater import MaterialCreater
from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.ownPopup import OwnPopup
from reinforcement.shapeSelection import ShapeSelection
from ownComponents.numpad import Numpad


class ReinforcementEditor(GridLayout, IObserver):
    
    '''
    the reinforcement-editor is the component, where you can edit the layers of a shape
    the shape-information is given by the cross-section-shape
    '''
    
    #cross-section
    cs = ObjectProperty()
    
    # strings
    densityStr, stiffnessStr = StringProperty('density[kg/m^3]:'), StringProperty('stiffness[MPa]:')
    priceStr, strengthStr = StringProperty('price[euro/m]:'), StringProperty('cracking stress [MPa]:')
    weightStr, areaStr = StringProperty('weight [kg/m]:'), StringProperty('area [m^2]: ')
    nameStr, steelStr = StringProperty('name:'), StringProperty('steel')
    rectangleStr, shapeStr = StringProperty('rectangle'), StringProperty('shape')
    materialStr, resetStr = StringProperty('material:'), StringProperty('-')
    ratioStr = StringProperty('reinforcement ratio [%]:')
    addStr, deleteStr = StringProperty('add layer'), StringProperty('delete layer')
    
    # constructor
    def __init__(self, **kwargs):
        super(ReinforcementEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 1, Design.spacing
        self.containsInformation, self.error = False, False
  
    '''
    create the gui
    '''

    def create_gui(self):
        # if you add more shapes, uncomment the follow row
        # self.create_selection_menu()
        self.create_cross_section_area()
        self.create_add_delete_area()
        self.create_material_information()
        self.create_add_layer_information_area()
        self.numpad = Numpad(p=self)
        self.popupNumpad = OwnPopup(title=self.areaStr, content=self.numpad)

    '''
    the method create_add_delete_area create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete_area(self):
        self.addDeleteLayout = GridLayout(cols=2, row_force_default=True,
                                          row_default_height=Design.btnHeight,
                                          size_hint_y=None, height=Design.btnHeight,
                                          spacing=Design.spacing)
        btnAdd = OwnButton(text=self.addStr)
        btnDelete = OwnButton(text=self.deleteStr)
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
        self.lblName, self.lblRatio = OwnLabel(text=self.resetStr), OwnLabel(text=self.resetStr)
        self.lblDensity, self.lblStiffness = OwnLabel(text=self.resetStr), OwnLabel(text=self.resetStr)
        self.lblStrength, self.areaInput = OwnLabel(text=self.resetStr), OwnButton(text=self.resetStr)
        self.areaInput.bind(on_press=self.show_numpad)
        materialLayout = GridLayout(cols=4, row_force_default=True,
                                    row_default_height=3 * Design.lblHeight,
                                    height=Design.btnHeight)
        materialLayout.add_widget(OwnLabel(text=self.nameStr))
        materialLayout.add_widget(self.lblName)
        materialLayout.add_widget(OwnLabel(text=self.ratioStr))
        materialLayout.add_widget(self.lblRatio)
        materialLayout.add_widget(OwnLabel(text=self.densityStr))
        materialLayout.add_widget(self.lblDensity)
        materialLayout.add_widget(OwnLabel(text=self.stiffnessStr))
        materialLayout.add_widget(self.lblStiffness)
        materialLayout.add_widget(OwnLabel(text='strength[MPa]'))
        materialLayout.add_widget(self.lblStrength)
        materialLayout.add_widget(OwnLabel(text=self.areaStr))
        materialLayout.add_widget(self.areaInput)
        self.materialLayout.add_widget(materialLayout)
        self.add_widget(self.materialLayout)

    '''
    the method create_cross_section_area create the area where you can 
    see the information of the cs_view
    '''

    def create_cross_section_area(self):
        self.lblcsPrice = OwnLabel(text=self.resetStr)
        self.lblcsWeight = OwnLabel(text=self.resetStr)
        self.lblcsStrength = OwnLabel(text=self.resetStr)
        self.csLayout = GridLayout(cols=2, row_force_default=True,
                                   row_default_height=3 * Design.lblHeight,
                                   height=2 * Design.lblHeight)
        self.csLayout.add_widget(OwnLabel(text=self.priceStr))
        self.csLayout.add_widget(self.lblcsPrice)
        self.csLayout.add_widget(OwnLabel(text=self.weightStr))
        self.csLayout.add_widget(self.lblcsWeight)
        self.csLayout.add_widget(OwnLabel(text=self.strengthStr))
        self.csLayout.add_widget(self.lblcsStrength)
        self.add_widget(self.csLayout)

    '''
    the method create_add_layer_information_area create the area where you can 
    add new materials
    '''

    def create_add_layer_information_area(self):
        self.create_material_options()
        btnConfirm = OwnButton(text='confirm')
        btnCancel = OwnButton(text='cancel')
        btnConfirm.bind(on_press=self.add_layer)
        btnCancel.bind(on_press=self.cancel_adding)
        self.addLayout = GridLayout(cols=2, row_force_default=True,
                                    row_default_height=Design.btnHeight,
                                    size_hint_y=None, height=4.5 * Design.btnHeight,
                                    spacing=Design.spacing)
        self.addLayout.add_widget(OwnLabel(text=self.materialStr))
        self.btnMaterialOption = OwnButton(text=self.steelStr)
        self.btnMaterialOption.bind(on_release=self.popup.open)
        self.addLayout.add_widget(self.btnMaterialOption)
        self.lblMaterialPercent = OwnLabel(text=self.areaStr)
        self.addLayout.add_widget(self.lblMaterialPercent)
        self.areaBtn = OwnButton(text='0.0')
        self.areaBtn.bind(on_press=self.show_numpad)
        self.addLayout.add_widget(self.areaBtn)
        self.addLayout.add_widget(btnConfirm)
        self.addLayout.add_widget(btnCancel)
        

    '''
    the method create_material_options create the popup where you can 
    select the materials for the new layer
    '''

    def create_material_options(self):
        self.materialSelectionLayout = GridLayout(cols=1, spacing=Design.spacing,
                                                  size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.materialSelectionLayout .bind(minimum_height=self.materialSelectionLayout.setter('height'))
        self.materialEditor = MaterialCreater()
        self.materialEditor.p = self
        self.popupMaterialEditor = OwnPopup(title='editor', content=self.materialEditor)
        for i in range(0, len(self.allMaterials.allMaterials) - 1):
            btnMaterialA = OwnButton(text=self.allMaterials.allMaterials[i].name)
            btnMaterialA.bind(on_press=self.select_material)
            self.materialSelectionLayout.add_widget(btnMaterialA)
        self.btnMaterialEditor = OwnButton(text='create material')
        self.btnMaterialEditor.bind(on_press=self.popupMaterialEditor.open)
        self.materialSelectionLayout.add_widget(self.btnMaterialEditor)
        self.root = ScrollView()
        self.root.add_widget(self.materialSelectionLayout)
        popupContent = GridLayout(cols=1)
        popupContent.add_widget(self.root)
        self.popup = OwnPopup(title=self.materialStr, content=popupContent)
    
    '''
    create the layout where you can select the cross-section-shape
    '''

    def create_selection_menu(self):
        self.create_popup_shape()
        selectionContent = GridLayout(cols=2, height=Design.btnHeight,
                                      size_hint_y=None, row_force_default=True,
                                      row_default_height=Design.btnHeight)
        self.btnSelection = OwnButton(text=self.rectangleStr)
        self.btnSelection.bind(on_press=self.show_shape_selection)
        selectionContent.add_widget(OwnLabel(text=self.shapeStr))
        selectionContent.add_widget(self.btnSelection)
        self.add_widget(selectionContent)
    
    '''
    create popup where you can select the shape of the cross section
    '''

    def create_popup_shape(self):
        shapeContent = ShapeSelection(information=self)
        self.shapeSelection = OwnPopup(title=self.shapeStr, content=shapeContent)
    
    '''
    open the popup where the user can select the shape
    '''

    def show_shape_selection(self, btn):
        self.shapeSelection.open()
    
    '''
    look which shape the user has selected
    '''

    def finished_shape_selection(self, btn):
        if btn.text == self.rectangleStr:
            self.btnSelection.text = btn.text
            self.cs.show_rectangle_view()
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
        self.remove_widget(self.csLayout)
        self.remove_widget(self.information)
        self.remove_widget(self.addDeleteLayout)
        self.add_widget(self.addLayout, 0)

    '''
    the method finished_adding was developed to hide the 
    the addLayout and show the materialLayout
    '''

    def finished_adding(self):
        self.remove_widget(self.addLayout)
        self.add_widget(self.materialLayout, 0)
        self.add_widget(self.addDeleteLayout, 1)
        self.add_widget(self.csLayout, 2)
        self.add_widget(self.information, 3)

    '''
    the method add_layer add a new layer at the cross section
    it use the choosen slidePercent value
    '''

    def add_layer(self, button):
        self.finished_adding()
        v=float(self.areaBtn.text)
        if v<=0:
            return
        for i in range(0, len(self.allMaterials.allMaterials)):
            if self.allMaterials.allMaterials[i].name == self.btnMaterialOption.text:
                p = v / self.cs.size
                # proofs whether the layer is bigger as the cs
                if p > 1:
                    # wrong input
                    return
                self.cs.add_layer(p, self.allMaterials.allMaterials[i])
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
    the method update_layinfo was developed to update
    the information, when the user selected a other rectangle in the view
    '''

    def update_layinfo(self, name, price, density, stiffness, strength, percent):
        self.lblName.text, self.lblRatio.text = str(name), str(percent * 100)
        self.lblDensity.text = str(density)
        self.lblStiffness.text = str(stiffness)
        self.lblStrength.text = str(strength)
        self.areaInput.text = '%.2E' % Decimal(str(self.cs.h * self.cs.w * percent))
    
    '''
    reset the layer_information when no layer is focused
    '''
    def reset_layer_information(self):
        self.lblName.text = self.resetStr
        self.lblRatio.text = self.resetStr
        self.lblDensity.text = self.resetStr
        self.lblStiffness.text = self.resetStr
        self.lblStrength.text = self.resetStr
        self.areaInput.text = self.resetStr

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
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.allMaterials = self.cs.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
    
        
    '''
    open the numpad for the input
    '''
    def show_numpad(self, btn):
        self.focusBtn = btn
        self.popupNumpad.open()
    
    '''
    method when the user confirm the input
    '''
    def finished_numpad(self):
        v = float(self.numpad.lblTextinput.text)
        self.focusBtn.text = str(v)
        # if the percentage of the layer must change
        if self.focusBtn == self.areaInput:
            self.cs.view.update_percent(v / self.cs.size)
        self.popupNumpad.dismiss()
        
    '''
    close the numpad
    '''
    def close_numpad(self):
        self.popupNumpad.dismiss()
