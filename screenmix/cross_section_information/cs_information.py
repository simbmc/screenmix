'''
Created on 10.03.2016

@author: mkennert
'''
from material_editor.creater import Material_Creater
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from designClass.design import Design
from material_editor.iobserver import IObserver
from cross_section_information.shape_selection import ShapeSelection
from cross_section_information.doubleTInformation import DoubleTInformation
from cross_section_information.rectangleInformation import RectangleInformation

'''
the class Cross_Section_Information was developed to show 
the information of the cs_view
'''
class Cross_Section_Information(GridLayout, IObserver):
    
    #Constructor
    def __init__(self, **kwargs):
        super(Cross_Section_Information, self).__init__(**kwargs)
        self.cols=1
        self.focusCrossSection=None
        self.firstTimeDoubleT=True
        self.btnSize=Design.btnSize
    
    ########################################################################################################
    # The following part of code create only the graphical user interface                                  #
    ########################################################################################################
    
    '''
    create the gui of the information
    '''
    def create_gui(self):
        self.createPopUp_Shape()
        self.create_selectionMenu()
        self.add_widget(self.rectangleInformation)
        self.create_cross_section_area()
        self.create_add_delete_area()
        self.create_material_information()
        self.create_add_layer_information_area()
        self.create_confirm_cancel_area()
    
    '''
    create the layout where you can select the cross-section-shape
    '''
    def create_selectionMenu(self):
        selectionContent=GridLayout(cols=1,spacing=10, 
                                    size_hint_y=None,row_force_default=True, 
                                    row_default_height=self.btnSize)
        self.btn_selection=Button(text='rectangle',size_hint_y=None, height=self.btnSize,
                                  size_hint_x=None, width=200)
        self.btn_selection.bind(on_press=self.showShapeSelection)
        selectionContent.add_widget(self.btn_selection)
        self.add_widget(selectionContent)
    
    '''
    create popup where you can select the shape of the cross section
    '''
    def createPopUp_Shape(self):
        shapeContent=ShapeSelection()
        shapeContent.setInformation(self)
        self.shapeSelection=Popup(title='shape',content=shapeContent)        
        
    '''
    the method create_add_delete_area create the area where you can 
    add new materials and delete materials from the cs_view
    '''
    def create_add_delete_area(self):
        self.btn_area=BoxLayout(orientation='horizontal')
        add_btn=Button(text='add layer',size_hint_y=None, height=self.btnSize)
        add_btn.bind(on_press=self.show_add_layer_area)
        delete_btn=Button(text='delete layer',size_hint_y=None, height=self.btnSize)
        delete_btn.bind(on_press=self.delete_layer)
        self.btn_area.add_widget(add_btn)
        self.btn_area.add_widget(delete_btn)
        self.add_widget(self.btn_area)
    
    '''
    the method create_material_information create the area where you can 
    see the information about the selected materials
    '''
    def create_material_information(self):
        self.material_area=GridLayout(cols=1)
        self.material_name=Label(text='-')
        self.material_price=Label(text='-')
        self.material_density=Label(text='-')
        self.material_stiffness=Label(text='-')
        self.material_strength=Label(text='-')
        self.material_percent=Label(text='10 %')
        label_layout=GridLayout(cols=4)
        label_layout.add_widget(Label(text='name:'))
        label_layout.add_widget(self.material_name)
        label_layout.add_widget(Label(text='price:'))
        label_layout.add_widget(self.material_price)
        label_layout.add_widget(Label(text='density:'))
        label_layout.add_widget(self.material_density)
        label_layout.add_widget(Label(text='stiffness:'))
        label_layout.add_widget(self.material_stiffness)
        label_layout.add_widget(Label(text='tensile strength:'))
        label_layout.add_widget(self.material_strength)
        label_layout.add_widget(Label(text='percent:'))
        label_layout.add_widget(self.material_percent)
        self.percent_value=Slider(min=0.05, max=0.2, value=0.1)
        self.percent_value.bind(value=self.set_percent)
        self.material_area.add_widget(label_layout)
        self.material_area.add_widget(self.percent_value)
        self.add_widget(self.material_area)
    
    '''
    the method create_cross_section_area create the area where you can 
    see the information of the cs_view
    '''
    def create_cross_section_area(self):
        self.cross_section_price=Label(text='-')
        self.cross_section_weight=Label(text='-')
        self.cross_section_strength=Label(text='-')
        self.cross_section_area=GridLayout(cols=2)
        self.cross_section_area.add_widget(Label(text='price [Euro/m]:'))
        self.cross_section_area.add_widget(self.cross_section_price)
        self.cross_section_area.add_widget(Label(text='weight [kg]:'))
        self.cross_section_area.add_widget(self.cross_section_weight)
        self.cross_section_area.add_widget(Label(text='tensile strength [MPa]:'))
        self.cross_section_area.add_widget(self.cross_section_strength)
        self.add_widget(self.cross_section_area)
    
    '''
    the method create_add_layer_information_area create the area where you can 
    add new materials
    '''
    def create_add_layer_information_area(self):
        self.create_material_options()
        self.adding_material_area=GridLayout(cols=2)
        self.adding_material_area.add_widget(Label(text='Material:'))
        self.material_option=Button(text='steel',size_hint_y=None, height=self.btnSize)
        self.material_option.bind(on_release=self.popup.open)
        self.adding_material_area.add_widget(self.material_option)
        self.material_percent_while_creating=Label(text='percent: 10%')
        self.adding_material_area.add_widget(self.material_percent_while_creating)
        self.slider_layer_percent=Slider(min=0.05,max=0.2,value=0.1)
        self.slider_layer_percent.bind(value=self.set_percenet_while_creating)
        self.adding_material_area.add_widget(self.slider_layer_percent)
    
    '''
    the method create_material_options create the popup where you can 
    select the materials for the new layer
    '''
    def create_material_options(self):
        self.layout_materials=GridLayout(cols=3)
        self.material_editor=Material_Creater()
        self.material_editor.sign_in_parent(self)
        self.popup_material_editor=Popup(title='editor',content=self.material_editor)
        for i in range(0,self.all_materials.get_length()):
            btn_material_A=Button(text=self.all_materials.all_materials[i].name)
            btn_material_A.bind(on_press=self.select_material)
            self.layout_materials.add_widget(btn_material_A)
        self.btn_material_editor=Button(text='create material')
        self.btn_material_editor.bind(on_press=self.popup_material_editor.open)
        self.layout_materials.add_widget(self.btn_material_editor)
        self.popup=Popup(title='materials',content=self.layout_materials)
    
    '''
    the method create_confirm_cancel_area create the area where you can 
    confirm your creation of the new materials or cancel the creation
    '''
    def create_confirm_cancel_area(self):
        self.confirm_cancel_area=BoxLayout()
        confirm_btn=Button(text='confirm',size_hint_y=None, height=self.btnSize)
        confirm_btn.bind(on_press=self.add_layer)
        cancel_btn=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        cancel_btn.bind(on_press=self.cancel_adding)
        self.confirm_cancel_area.add_widget(confirm_btn)
        self.confirm_cancel_area.add_widget(cancel_btn)
    
    ########################################################################################################
    ########################################################################################################
    
    '''
    the method show_add_layer_area was developed to show the 
    the adding_material_area and hide the material_information
    '''
    def show_add_layer_area(self, button):
        self.remove_widget(self.material_area)
        self.remove_widget(self.btn_area)
        self.slider_layer_percent.value=0.1
        self.add_widget(self.adding_material_area,0)
        self.add_widget(self.confirm_cancel_area, 1)
    
    '''
    the method finished_adding was developed to hide the 
    the adding_material_area and show the material_area
    '''
    def finished_adding(self):
        self.remove_widget(self.adding_material_area)
        self.remove_widget(self.confirm_cancel_area)
        self.add_widget(self.material_area,0)
        self.add_widget(self.btn_area,1)
    
    '''
    the method add_layer add a new layer at the cross section
    it use the choosen percent value
    '''
    def add_layer(self,button):
        self.finished_adding()
        for i in range(0,self.all_materials.get_length()):
            if self.all_materials.all_materials[i].name==self.material_option.text:
                self.cross_section.add_layer(self.slider_layer_percent.value,self.all_materials.all_materials[i])
                return
    '''
    the method cancel_adding would be must call when the user wouldn't 
    add a new materials
    '''
    def cancel_adding(self,button):
        self.finished_adding()
    
    '''
    the method delete_layer was developed to delete a existing
    materials
    '''
    def delete_layer(self, button):
        self.cross_section.delete_layer()
    
    '''
    the method update_layer_information was developed to update
    the information, when the user selected a other rectangle in the view
    '''
    def update_layer_information(self,name,price,density,stiffness,strength,percent):
        self.material_name.text=str(name)
        self.material_price.text=str(price)
        self.material_density.text=str(density)
        self.material_stiffness.text=str(stiffness)
        self.material_strength.text=str(strength)
        self.percent_value.value=percent
    
    '''
    the method update_cross_section_information update the cross section information.
    '''
    def update_cross_section_information(self,price, weight,strength):
        self.cross_section_price.text=str(price)
        self.cross_section_weight.text=str(weight)
        self.cross_section_strength.text=str(strength)
    
    '''
    the method cancel_edit_material cancel the editing of the material
    and reset the values of the material_editor
    '''
    def cancel_edit_material(self):
        self.popup_material_editor.dismiss()
        self.material_editor.reset_editor()
        
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''
    def update(self):
        self.layout_materials.remove_widget(self.btn_material_editor)
        btn_material_A=Button(text=self.all_materials.all_materials[-1].name)
        btn_material_A.bind(on_press=self.select_material)
        self.layout_materials.add_widget(btn_material_A)
        self.layout_materials.add_widget(self.btn_material_editor)
        
    '''
    look which shape the user has selected
    '''
    def finishedShapeSelection(self,btn):
        if btn.text=='circle':
            #not finished yet
            pass
        elif btn.text=='rectangle':
            self.setRectangle(btn)
        elif btn.text=='doubleT':
            self.setDoubleT(btn)
    
    '''
    open the popup where the user can select the shape
    ''' 
    def showShapeSelection(self,btn):
        self.shapeSelection.open()
    
    #################################################################################################
    #                                Setter && Getter                                               #
    #################################################################################################
    
    '''
    the method will be called when the user selected a material
    the popup will be closed and the button text change to the material
    name
    '''
    def select_material(self, Button):
        self.popup.dismiss()
        self.material_option.text=Button.text
    
    '''
    the method set_percent change the percentage share 
    of the materials. 
    Attention: this method must be call when the materials already exist
    '''
    def set_percent(self, instance, value):
        self.cross_section.set_percent(value)
        self.material_percent.text=str(int(value*100))+' %'
    
    '''
    the method set_percenet_while_creating change the percentage share 
    of the materials. Attention: this method must be call 
    when the materials isn't exist
    '''
    def set_percenet_while_creating(self,instance,value):
        self.material_percent_while_creating.text='percent: '+str(int(value*100))+' %'
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,allCrossSections):
        self.allCrossSections=allCrossSections
        #default cross section rectangle
        self.cross_section=allCrossSections.getCSRectangle()
        self.rectangleInformation=RectangleInformation()
        self.focusCrossSection=self.rectangleInformation
        self.rectangleInformation.setCrossSection(self.cross_section)
        self.all_materials=self.allCrossSections.all_materials
        self.all_materials.add_listener(self)
        self.create_gui()
    
    '''
    change the current cross section
    '''
    def change_CrossSection(self,cross_section):
        self.cross_section=cross_section
        
    '''
    show the rectangle shape
    '''
    def setRectangle(self, btn):
        self.btn_selection.text=btn.text
        self.cross_section=self.allCrossSections.getCSRectangle()
        self.remove_widget(self.focusCrossSection)
        self.focusCrossSection=self.rectangleInformation
        self.add_widget(self.rectangleInformation,3)
        self.allCrossSections.showRectangleView()
        self.shapeSelection.dismiss()
    
    '''
    show the doubleT shape
    '''
    def setDoubleT(self,btn):
        self.btn_selection.text=btn.text
        self.cross_section=self.allCrossSections.getCSDoubleT()
        if self.firstTimeDoubleT:
            self.doubleTInformation=DoubleTInformation()
            self.doubleTInformation.setCrossSection(self.cross_section)
            self.firstTimeDoubleT=False
        self.remove_widget(self.focusCrossSection)
        self.focusCrossSection=self.doubleTInformation
        self.add_widget(self.doubleTInformation,3)
        self.allCrossSections.showDoubleTView()
        self.shapeSelection.dismiss()
    
    '''
    show the circle shape
    '''
    #not finished yet
    def setCircle(self,btn):
        self.btn_selection.text=btn.text
        #not finished yet
        #self.cross_section=self.allCrossSections.getCSCircle()
        self.shapeSelection.dismiss()
    