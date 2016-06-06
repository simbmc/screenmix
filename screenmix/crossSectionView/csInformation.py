'''
Created on 06.06.2016

@author: mkennert
'''
from materialEditor.editor import Material_Editor
'''
Created on 10.03.2016
@author: mkennert
'''
from materialEditor.creater import Material_Creater
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from designClass.design import Design
'''
the class Cross_Section_Information was developed to show 
the information of the cs_view
'''
class Cross_Section_Information(BoxLayout):
    
    #Constructor
    def __init__(self, **kwargs):
        super(Cross_Section_Information, self).__init__(**kwargs)
        self.orientation='vertical'
        self.btnSize=Design.btnSize
        
        
    
    ########################################################################################################
    # The following part of code create only the graphical user interface                                  #
    ########################################################################################################
    
    #not finished yet
    def create_gui(self):
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
        self.scale_area=GridLayout(cols=2)
        #adding_material_area to manage the height-area
        self.height_value=Label(text='height: 0.5 m',size_hint_x=None, width=100)
        slider_height=Slider(min=0.1, max=0.5, value=0.5)
        slider_height.bind(value=self.set_height)
        self.scale_area.add_widget(self.height_value)
        self.scale_area.add_widget(slider_height)
        #adding_material_area to manage the width-area
        self.width_value=Label(text='width: 0.25 m',size_hint_x=None, width=100)
        slider_width=Slider(min=0.1, max=0.5, value=0.25)
        slider_width.bind(value=self.set_width)
        self.scale_area.add_widget(self.width_value)
        self.scale_area.add_widget(slider_width)
        self.add_widget(self.scale_area)
    
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
    the method set_height change the height of the cs_view
    '''
    def set_height(self, instance, value):
        self.cross_section.set_height(value)
        value=int(value*100)
        self.height_value.text='height: 0.'+str(value)+' m'
    
    '''
    the method set_width change the width of the cs_view
    '''
    def set_width(self, instance, value):
        self.cross_section.set_width(value)
        value=int(value*100)
        self.width_value.text='width: 0.'+str(value)+' m'
    
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
    def set_cross_section(self,cross_section):
        self.cross_section=cross_section
        self.all_materials=self.cross_section.all_materials
        self.all_materials.add_listener(self)
        self.create_gui()