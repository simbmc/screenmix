'''
Created on 06.06.2016

@author: mkennert
'''
'''
Created on 10.03.2016
@author: mkennert
'''
'''
the class CrossSectionInformation was developed to show 
the information of the cs_view
'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

from designClass.design import Design
from materialEditor.creater import MaterialCreater
from materialEditor.editor import Material_Editor
from materialEditor.numpad import Numpad


class CrossSectionInformation(BoxLayout):

    # Constructor
    def __init__(self, **kwargs):
        super(CrossSectionInformation, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.btnSize = Design.btnSize
        self.focusBtn = None

    ##########################################################################
    # The following part of code create only the graphical user interface                                  #
    ##########################################################################

    '''
    create the gui
    '''
    def create_gui(self):
        self.create_numpad()
        self.create_scale_area()
        self.create_cross_section_area()
        self.create_add_delete_area()
        self.create_material_information()
        self.create_add_layer_information_area()
        self.create_confirm_cancel_area()

    '''
    the method create_scale_area create the area where you can 
    scale the height and the width of the cs_view
    '''

    def create_scale_area(self):
        self.scaleArea = GridLayout(cols=2)
        # addingMaterialArea to manage the height-area
        self.heightValue = Label(text='height [m]')
        self.btnHeight = Button(text='0.5')
        self.btnHeight.bind(on_press=self.show_numpad)
        self.btnWidth = Button(text='0.25')
        self.btnWidth.bind(on_press=self.show_numpad)
        self.scaleArea.add_widget(self.heightValue)
        self.scaleArea.add_widget(self.btnHeight)
        # addingMaterialArea to manage the width-area
        self.widthValue = Label(text='width [m]')
        self.scaleArea.add_widget(self.widthValue)
        self.scaleArea.add_widget(self.btnWidth)
        self.add_widget(self.scaleArea)

    '''
    the method create_add_delete_area create the area where you can 
    add new materials and delete materials from the cs_view
    '''

    def create_add_delete_area(self):
        self.btnArea = BoxLayout(orientation='horizontal')
        addBtn = Button(
            text='add layer', size_hint_y=None, height=self.btnSize)
        addBtn.bind(on_press=self.show_add_layer_area)
        deleteBtn = Button(
            text='delete layer', size_hint_y=None, height=self.btnSize)
        deleteBtn.bind(on_press=self.delete_layer)
        self.btnArea.add_widget(addBtn)
        self.btnArea.add_widget(deleteBtn)
        self.add_widget(self.btnArea)

    '''
    the method create_material_information create the area where you can 
    see the information about the selected materials
    '''

    def create_material_information(self):
        self.materialArea = GridLayout(cols=1)
        self.materialName = Label(text='-')
        self.materialPrice = Label(text='-')
        self.materialDensity = Label(text='-')
        self.materialStiffness = Label(text='-')
        self.materialStrength = Label(text='-')
        self.materialPercent = Label(text='10 %')
        labelLayout = GridLayout(cols=4)
        labelLayout.add_widget(Label(text='name:'))
        labelLayout.add_widget(self.materialName)
        labelLayout.add_widget(Label(text='price:'))
        labelLayout.add_widget(self.materialPrice)
        labelLayout.add_widget(Label(text='density:'))
        labelLayout.add_widget(self.materialDensity)
        labelLayout.add_widget(Label(text='stiffness:'))
        labelLayout.add_widget(self.materialStiffness)
        labelLayout.add_widget(Label(text='tensile strength:'))
        labelLayout.add_widget(self.materialStrength)
        labelLayout.add_widget(Label(text='percent:'))
        labelLayout.add_widget(self.materialPercent)
        self.percentValue = Slider(min=0.05, max=0.2, value=0.1)
        self.percentValue.bind(value=self.set_percent)
        self.materialArea.add_widget(labelLayout)
        self.materialArea.add_widget(self.percentValue)
        self.add_widget(self.materialArea)

    '''
    the method create_cross_section_area create the area where you can 
    see the information of the cs_view
    '''

    def create_cross_section_area(self):
        self.crossSectionPrice = Label(text='-')
        self.crossSectionWeight = Label(text='-')
        self.crossSectionStrength = Label(text='-')
        self.crossSectionArea = GridLayout(cols=2)
        self.crossSectionArea.add_widget(Label(text='price [Euro/m]:'))
        self.crossSectionArea.add_widget(self.crossSectionPrice)
        self.crossSectionArea.add_widget(Label(text='weight [kg]:'))
        self.crossSectionArea.add_widget(self.crossSectionWeight)
        self.crossSectionArea.add_widget(Label(text='tensile strength [MPa]:'))
        self.crossSectionArea.add_widget(self.crossSectionStrength)
        self.add_widget(self.crossSectionArea)

    '''
    the method create_add_layer_information_area create the area where you can 
    add new materials
    '''

    def create_add_layer_information_area(self):
        self.create_material_options()
        self.addingMaterialArea = GridLayout(cols=2)
        self.addingMaterialArea.add_widget(Label(text='Material:'))
        self.materialOption = Button(
            text='steel', size_hint_y=None, height=self.btnSize)
        self.materialOption.bind(on_release=self.popup.open)
        self.addingMaterialArea.add_widget(self.materialOption)
        self.materialPercentWhileCreating = Label(text='percent: 10%')
        self.addingMaterialArea.add_widget(self.materialPercentWhileCreating)
        self.sliderLayerPercent = Slider(min=0.05, max=0.2, value=0.1)
        self.sliderLayerPercent.bind(value=self.set_percenet_while_creating)
        self.addingMaterialArea.add_widget(self.sliderLayerPercent)

    '''
    the method create_material_options create the popup where you can 
    select the materials for the new layer
    '''

    def create_material_options(self):
        self.layoutMaterials  = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.layoutMaterials .bind(minimum_height=self.layoutMaterials.setter('height'))
        self.materialEditor = MaterialCreater()
        self.materialEditor.sign_in_parent(self)
        self.popupMaterialEditor = Popup(
            title='editor', content=self.materialEditor)
        for i in range(0, self.allMaterials.get_length()):
            btnMaterialA = Button(text=self.allMaterials.allMaterials[i].name, size_hint_y=None, height=self.btnSize)
            btnMaterialA.bind(on_press=self.select_material)
            self.layoutMaterials.add_widget(btnMaterialA)
        self.btnMaterialEditor = Button(text='create material', size_hint_y=None, height=self.btnSize)
        self.btnMaterialEditor.bind(on_press=self.popupMaterialEditor.open)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)
        self.root = ScrollView()
        self.root.add_widget(self.layoutMaterials)
        self.popup = Popup(title='materials', content=self.root)

    '''
    the method create_confirm_cancel_area create the area where you can 
    confirm your creation of the new materials or cancel the creation
    '''

    def create_confirm_cancel_area(self):
        self.confirmCancelArea = BoxLayout()
        confirmBtn = Button(
            text='confirm', size_hint_y=None, height=self.btnSize)
        confirmBtn.bind(on_press=self.add_layer)
        cancelBtn = Button(
            text='cancel', size_hint_y=None, height=self.btnSize)
        cancelBtn.bind(on_press=self.cancel_adding)
        self.confirmCancelArea.add_widget(confirmBtn)
        self.confirmCancelArea.add_widget(cancelBtn)

    '''
    create the numpad
    '''

    def create_numpad(self):
        self.numpad = Numpad()
        self.numpad.sign_in_parent(self)
        self.popupNumpad = Popup(content=self.numpad)

    ##########################################################################
    ##########################################################################

    '''
    the method show_add_layer_area was developed to show the 
    the addingMaterialArea and hide the material_information
    '''

    def show_add_layer_area(self, button):
        self.remove_widget(self.materialArea)
        self.remove_widget(self.btnArea)
        self.sliderLayerPercent.value = 0.1
        self.add_widget(self.addingMaterialArea, 0)
        self.add_widget(self.confirmCancelArea, 1)

    '''
    the method finished_adding was developed to hide the 
    the addingMaterialArea and show the materialArea
    '''

    def finished_adding(self):
        self.remove_widget(self.addingMaterialArea)
        self.remove_widget(self.confirmCancelArea)
        self.add_widget(self.materialArea, 0)
        self.add_widget(self.btnArea, 1)

    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''

    def add_layer(self, button):
        self.finished_adding()
        for i in range(0, self.allMaterials.get_length()):
            if self.allMaterials.allMaterials[i].name == self.materialOption.text:
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
        self.materialName.text = str(name)
        self.materialPrice.text = str(price)
        self.materialDensity.text = str(density)
        self.materialStiffness.text = str(stiffness)
        self.materialStrength.text = str(strength)
        self.percentValue.value = percent

    '''
    the method update_cross_section_information update the cross section information.
    '''

    def update_cross_section_information(self, price, weight, strength):
        self.crossSectionPrice.text = str(price)
        self.crossSectionWeight.text = str(weight)
        self.crossSectionStrength.text = str(strength)

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
        self.layoutMaterials.remove_widget(self.btnMaterialEditor)
        btnMaterialA = Button(text=self.allMaterials.allMaterials[-1].name, size_hint_y=None, height=self.btnSize)
        btnMaterialA.bind(on_press=self.select_material)
        self.layoutMaterials.add_widget(btnMaterialA)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)

    '''
    show the numpad for the input
    '''

    def show_numpad(self, btn):
        self.popupNumpad.open()
        self.focusBtn = btn

    '''
    close the numpad 
    '''

    def closeNumpad(self):
        self.popupNumpad.dismiss()

    '''
    finish the numpad
    '''

    def finished_numpad(self):
        self.focusBtn.text = self.numpad.textinput.text
        if self.focusBtn.text == self.btnHeight:
            self.cs.set_height(float(self.focusBtn.text))
        else:
            self.cs.set_width(float(self.focusBtn.text))
        self.popupNumpad.dismiss()
    
    '''
    the method will be called when the user selected a material
    the popup will be closed and the button text change to the material
    name
    '''

    def select_material(self, Button):
        self.popup.dismiss()
        self.materialOption.text = Button.text

    ##########################################################################
    #                                Setter && Getter                        #
    ##########################################################################


    '''
    the method set_height change the height of the cs_view
    '''

    def set_height(self, instance, value):
        self.cs.set_height(value)
        value = int(value * 100)
        self.heightValue.text = 'height: 0.' + str(value) + ' m'

    '''
    the method set_width change the width of the cs_view
    '''

    def set_width(self, instance, value):
        self.cs.set_width(value)
        value = int(value * 100)
        self.widthValue.text = 'width: 0.' + str(value) + ' m'

    '''
    the method set_percent change the percentage share 
    of the materials. 
    Attention: this method must be call when the materials already exist
    '''

    def set_percent(self, instance, value):
        self.cs.set_percent(value)
        self.materialPercent.text = str(int(value * 100)) + ' %'

    '''
    the method set_percenet_while_creating change the percentage share 
    of the materials. Attention: this method must be call 
    when the materials isn't exist
    '''

    def set_percenet_while_creating(self, instance, value):
        self.materialPercentWhileCreating.text = 'percent: ' + \
            str(int(value * 100)) + ' %'

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.allMaterials = self.cs.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
