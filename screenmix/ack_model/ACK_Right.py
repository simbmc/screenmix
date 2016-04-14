'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from cross_section.Cross_Section import Cross_Section
from cross_section_view.CS_Rectangle_View import colorcycler
from kivy.garden.graph import Graph, MeshLinePlot 


class Ack_Right(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(Ack_Right, self).__init__(**kwargs)
        self.cols=1
    
    def create_gui(self):
        self.create_graph()
        self.create_option_layout()
        
    '''
    the method create_graph create the graph
    '''
    def create_graph(self):
        self.graph = Graph(
                        x_ticks_major=0.1, y_ticks_major=0.1,
                        y_grid_label=True, x_grid_label=True,
                        xmin=0.0, xmax=self.cross_section.cross_section_width, ymin=0, ymax=self.cross_section.cross_section_height)
        self.add_widget(self.graph)
    
    def create_option_layout(self):
        content_height=10
        content=GridLayout(cols=2,row_force_default=True, row_default_height=content_height, size_hint_y=None, height=25)
        slider_value=0.02
        self.strain=Label(text='strain: '+str(slider_value))
        slider=Slider(min=0, max=0.1,value=slider_value)
        slider.bind(value=self.setStrain)
        content.add_widget(self.strain)
        content.add_widget(slider)
        self.add_widget(content)
    
    def setStrain(self,instance,value):
        value=int(value*100000)
        self.strain.text='strain: 0.'+str(value)
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,cross_section):
        self.cross_section=cross_section
        self.create_gui()
    
class CSIApp(App):
    def build(self):
        ack=Ack_Right()
        return ack

if __name__ == '__main__':
    CSIApp().run()