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


class Cross_Section_Information(BoxLayout):
    #Components
    scale_area=GridLayout(cols=1)
    btn_area=BoxLayout(spacing=10, orientation='horizontal')
    material_area=GridLayout(cols=1)
    cross_section_area=GridLayout(cols=2)
    #Components of the scale_area
    height_value=Label(text='height: 0,25 m',size_hint_x=None, width=100)
    width_value=Label(text='width: 0,25 m',size_hint_x=None, width=100)
    #Components of material_information
    material_name=Label(text='-')
    material_price=Label(text='-')
    material_density=Label(text='-')
    material_stiffness=Label(text='-')
    material_strength=Label(text='-')
    material_percent=Label(text='10 %')
    #Components of cross_section_area
    cross_section_price=Label(text='-')
    cross_section_weight=Label(text='-')
    cross_section_strength=Label(text='-')
    
    def __init__(self, **kwargs):
        super(Cross_Section_Information, self).__init__(**kwargs)
        #self.cols=1
        self.orientation='vertical'
        self.create_scale_area()
        self.create_cross_section_area()
        self.create_btn_area()
        self.create_material_information()
    
    def create_scale_area(self):
        #layout to manage the height-area
        layout_height=GridLayout(cols=2)
        slider_height=Slider(min=10, max=50, value=25)
        slider_height.bind(value=self.set_height_value)
        layout_height.add_widget(self.height_value)
        layout_height.add_widget(slider_height)
        #layout to manage the width-area
        layout_width=GridLayout(cols=2)
        slider_width=Slider(min=10, max=50, value=25)
        slider_width.bind(value=self.set_width_value)
        layout_width.add_widget(self.width_value)
        layout_width.add_widget(slider_width)
        self.scale_area.add_widget(layout_height)
        self.scale_area.add_widget(layout_width)
        self.add_widget(self.scale_area)
        
    def create_btn_area(self):
        add_btn=Button(text='add material')
        add_btn.bind(on_press=self.add_material)
        delete_btn=Button(text='delete material')
        delete_btn.bind(on_press=self.delete_material)
        self.btn_area.add_widget(add_btn)
        self.btn_area.add_widget(delete_btn)
        self.add_widget(self.btn_area)
    
    def create_material_information(self):
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
    
    def create_cross_section_area(self):
        self.cross_section_area.add_widget(Label(text='price:'))
        self.cross_section_area.add_widget(self.cross_section_price)
        self.cross_section_area.add_widget(Label(text='weight:'))
        self.cross_section_area.add_widget(self.cross_section_weight)
        self.cross_section_area.add_widget(Label(text='strength:'))
        self.cross_section_area.add_widget(self.cross_section_strength)
        self.add_widget(self.cross_section_area)
    
    def set_height_value(self, instance, value):
        value=int(value)
        self.height_value.text='height: 0,'+str(value)+' m'
    
    def set_width_value(self, instance, value):
        value=int(value)
        self.width_value.text='width: 0,'+str(value)+' m'
    
    def set_percent(self, instance, value):
        value=int(value)
        self.material_percent.text=str(value)+' %'
    
    def add_material(self, button):
        print('add is not yet implemented')
        
    def delete_material(self, button):
        print('delete is not yet implemented')
    
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