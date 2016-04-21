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
from plot.filled_rect import FilledRect


class Ack_Right(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(Ack_Right, self).__init__(**kwargs)
        self.cols = 1

    def create_gui(self):
        self.create_graph()
        self.create_option_layout()

    '''
    the method create_graph create the graph
    '''

    def create_graph(self):
        self.graph = Graph(xlabel='stress [MPa]', ylabel='height [m]',
                           x_ticks_major=0.0001, y_ticks_major=0.1,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=0.0005, ymin=0, ymax=self.cross_section.cross_section_height)

        self.add_widget(self.graph)

    def create_option_layout(self):
        content_height = 30
        content = GridLayout(cols=2, row_force_default=True,
                             row_default_height=content_height, size_hint_y=None, height=content_height)
        slider_value = 0.02
        self.strain = Label(text='strain: ' + str(slider_value))
        self.slider = Slider(min=0.00001, max=0.1, value=slider_value)
        self.slider.bind(value=self.setStrain)
        content.add_widget(self.strain)
        content.add_widget(self.slider)
        self.add_widget(content)

    def setStrain(self, instance, value):
        self.strain.text = 'strain: ' + str(value)
        self.update()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cross_section):
        self.cross_section = cross_section
        self.create_gui()

    '''
    update the layerinformation of layers
    '''

    def update(self):
        self.find_max_stress()
        self.graph.ymax = self.cross_section.cross_section_height
        list = []
        for plot in self.graph.plots:
            list.append(plot)
        # draw the free places of the cross section
        free_places = self.cross_section.view.get_free_places()
        for layer in free_places:
            self.rect = FilledRect(xrange=[0, self.cross_section.calculate_strain_of_concrete() * self.slider.value],
                                   yrange=[layer[0], layer[1]],
                                   color=[255, 255, 255])
            self.graph.add_plot(self.rect)
        # draw the layers
        for layer in self.cross_section.view.layers:
            layer.rect = FilledRect(xrange=[0, layer.get_strain() * self.slider.value],
                                    yrange=[
                                        layer.y_coordinate - layer._height / 2., layer.y_coordinate + layer._height / 2.],
                                    color=layer.colors)
            self.graph.add_plot(layer.rect)
        # delete the old plots
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        return self.graph

    def find_max_stress(self):
        # ask Li for that
        self.max_stress = self.cross_section.concrete_stiffness * \
            self.slider.value

        for layer in self.cross_section.view.layers:
            cur_value = layer.material.stiffness * self.slider.value
            if self.max_stress < cur_value:
                self.max_stress = cur_value
        self.graph.xmax = self.max_stress
        self.graph.x_ticks_major = int(self.max_stress / 5.)


class CSIApp(App):

    def build(self):
        ack = Ack_Right()
        cs = Cross_Section()
        ack.set_cross_section(cs)
        return ack

if __name__ == '__main__':
    CSIApp().run()
