'''
Created on 10.03.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from numpy import spacing
from cgitb import text

'''
the class Cross_Section_Information was developed to show 
the information of the cs_view
'''
class Cross_Section_Information(BoxLayout):
    
    #Constructor
    def __init__(self, **kwargs):
        super(Cross_Section_Information, self).__init__(**kwargs)
        #self.cols=1
        self.orientation='vertical'
        self.create_scale_area()
        self.create_cross_section_area()
        self.create_btn_area()
        self.create_material_information()
        self.create_add_area()
    
    '''
    the method create_scale_area create the area where you can 
    scale the height and the width of the cs_view
    '''
    def create_scale_area(self):
        self.scale_area=GridLayout(cols=1)
        #adding_area to manage the height-area
        self.height_value=Label(text='height: 0,25 m',size_hint_x=None, width=100)
        layout_height=GridLayout(cols=2)
        slider_height=Slider(min=10, max=50, value=25)
        slider_height.bind(value=self.set_height_value)
        layout_height.add_widget(self.height_value)
        layout_height.add_widget(slider_height)
        #adding_area to manage the width-area
        layout_width=GridLayout(cols=2)
        self.width_value=Label(text='width: 0,25 m',size_hint_x=None, width=100)
        slider_width=Slider(min=10, max=50, value=25)
        slider_width.bind(value=self.set_width_value)
        layout_width.add_widget(self.width_value)
        layout_width.add_widget(slider_width)
        self.scale_area.add_widget(layout_height)
        self.scale_area.add_widget(layout_width)
        self.add_widget(self.scale_area)
    
    '''
    the method create_btn_area create the area where you can 
    add new material and delete material from the cs_view
    '''
    def create_btn_area(self):
        self.btn_area=BoxLayout(spacing=10, orientation='horizontal')
        add_btn=Button(text='add material')
        add_btn.bind(on_press=self.add_material)
        delete_btn=Button(text='delete material')
        delete_btn.bind(on_press=self.delete_material)
        self.btn_area.add_widget(add_btn)
        self.btn_area.add_widget(delete_btn)
        self.add_widget(self.btn_area)
    
    '''
    the method create_material_information create the area where you can 
    see the information about the selected material
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
        label_layout.add_widget(Label(text='strength:'))
        label_layout.add_widget(self.material_strength)
        label_layout.add_widget(Label(text='percent:'))
        label_layout.add_widget(self.material_percent)
        percent_value=Slider(min=5, max=20, value=10)
        percent_value.bind(value=self.set_percent)
        self.material_area.add_widget(label_layout)
        self.material_area.add_widget(percent_value)
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
        self.cross_section_area.add_widget(Label(text='price:'))
        self.cross_section_area.add_widget(self.cross_section_price)
        self.cross_section_area.add_widget(Label(text='weight:'))
        self.cross_section_area.add_widget(self.cross_section_weight)
        self.cross_section_area.add_widget(Label(text='strength:'))
        self.cross_section_area.add_widget(self.cross_section_strength)
        self.add_widget(self.cross_section_area)
    
    '''
    the method create_add_area create the area where you can 
    add new material
    '''
    #not finished yet
    def create_add_area(self):
        self.adding_area=GridLayout(cols=2)
        self.adding_area.add_widget(Label(text='material:'))
        #combobox
        self.adding_area.add_widget(Label(text='percent: 10%'))
        #slider
        confirm_btn=Button(text='confirm')
        confirm_btn.bind(on_press=self.create_new_material)
        cancel_btn=Button(text='cancel')
        cancel_btn.bind(on_press=self.cancel_adding)
        self.adding_area.add_widget(confirm_btn)
        self.adding_area.add_widget(cancel_btn)
    
    '''
    the method set_height_value change the height of the cs_view
    '''
    #not finished yet
    def set_height_value(self, instance, value):
        value=int(value)
        self.height_value.text='height: 0,'+str(value)+' m'
    
    '''
    the method set_width_value change the width of the cs_view
    '''
    #not finished yet
    def set_width_value(self, instance, value):
        value=int(value)
        self.width_value.text='width: 0,'+str(value)+' m'
    
    '''
    the method set_height_value change the percentage share 
    of the material
    '''
    #not finished yet
    def set_percent(self, instance, value):
        value=int(value)
        self.material_percent.text=str(value)+' %'
    
    '''
    the method add_material was developed to show the 
    the adding_area and hide the material_area
    '''
    def add_material(self, button):
        self.remove_widget(self.material_area)
        self.add_widget(self.adding_area,0)
    
    
    '''
    the method delete_material was developed to delete a existing
    material
    '''
    #not yet implemented    
    def delete_material(self, button):
        print('delete is not yet implemented')
    
    '''
    the method finished_adding was developed to hide the 
    the adding_area and show the material_area
    '''
    def finished_adding(self):
        self.remove_widget(self.adding_area)
        self.add_widget(self.material_area,0)
    
    '''
    the method create_new_material
    '''
    #not yet implemented
    def create_new_material(self,button):
        self.finished_adding()
        print('add new material is not yet implemented')
    
    '''
    the methode cancel_adding would be must call when the user wouldn't 
    add a new material
    '''
    def cancel_adding(self,button):
        self.finished_adding()
        
    
#Just for testing
class CSIApp(App):
    def build(self):
        layout=GridLayout(cols=2)
        layout.add_widget(Button(text='view'))
        csi=Cross_Section_Information()
        layout.add_widget(csi)
        return layout


if __name__ == '__main__':
    CSIApp().run()