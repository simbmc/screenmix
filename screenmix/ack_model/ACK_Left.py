'''
Created on 12.04.2016

@author: mkennert
'''
from itertools import cycle

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from cross_section_view.CS_Rectangle_View import colorcycler
from kivy.garden.graph import Graph, MeshLinePlot
from cross_section.Cross_Section import Cross_Section


class Ack_Left(GridLayout):
    colors = [0.8, 0.3, 0.5, 0.2, 0.1, 0.7, 0.1]
    colorcycler = cycle(colors)
    # Constructor

    def __init__(self, **kwargs):
        super(Ack_Left, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.create_option_layout()

    '''
    the method create_graph create the graph
    '''

    def create_graph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=0.0001, y_ticks_major=5,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=0.01, ymin=0, ymax=30)
        self.add_widget(self.graph)

    '''
    the method create_option_layout create gui-part without the graph
    '''

    def create_option_layout(self):
        self.option_layout = GridLayout(cols=2)
#         self.option_layout.add_widget(Label(text='bond [N/mm]:'))
#         self.bond_slider = Slider()
#         self.option_layout.add_widget(self.bond_slider)
        self.plot_btn = Button(text='plot')
        self.plot_btn.bind(on_press=self.plot)
        self.clear_btn = Button(text='clear')
        self.clear_btn.bind(on_press=self.clear)
        self.option_layout.add_widget(self.plot_btn)
        self.option_layout.add_widget(self.clear_btn)
        self.add_widget(self.option_layout)

    '''
    the method plot plots a curve
    '''

    def plot(self, button):
        self.plot = MeshLinePlot(
            color=[next(colorcycler), next(colorcycler), next(colorcycler), 1])
        self.plot.points = self.calculate_points()
        self.graph.add_plot(self.plot)

    '''
    the method alculate_points calculate the points for 
    the graphh 
    '''

    def calculate_points(self):
        points = [(0, 0)]
        points.append(
            (self.cross_section.min_of_maxstrain, self.cross_section.strength))

        if self.cross_section.view.layers:
            # calculate the second points
            # calculate the stiffness of the reinforcement layers according to
            # mixture rule
            percent_of_layers = 0.  # the sum of the percentage of the reinforcement layers
            for layer in self.cross_section.view.layers:
                percent_of_layers += layer.percentage
            # stiffness of the section
            E_s = self.cross_section.strength / \
                self.cross_section.min_of_maxstrain
            E_r = 0.  # the stiffness of the reinforement mixture
            for layer in self.cross_section.view.layers:
                E_r += layer.material.stiffness * \
                    layer.percentage / percent_of_layers
            # the reinforcement strain at the crack postion
            eps_r_max = self.cross_section.min_of_maxstrain * \
                E_s / (E_r * percent_of_layers)
            # the minimum reinforcement strain
            eps_r_min = eps_r_max - 0.6685 * \
                (1 - percent_of_layers) * self.cross_section.concrete_strength / \
                (percent_of_layers * E_r)
            eps_r_avg = (eps_r_max + eps_r_min) / 2.
            points.append((eps_r_avg, self.cross_section.strength))

            # calculate the third points
            # the maximum reinforcement strain
            max_strain_r = 1e8
            for layer in self.cross_section.view.layers:
                cur_strain = layer.get_strain()
                max_strain_r = min(cur_strain, max_strain_r)
            # maximum composite strength
            max_strangth_c = E_r * max_strain_r * percent_of_layers
            # maximum composite strain
            max_strain_c = eps_r_avg + (max_strain_r - eps_r_max)
            points.append((max_strain_c, max_strangth_c))

        # setting the maximum of the graph
        self.graph.xmax = points[-1][0] * 1.2
        self.graph.ymax = points[-1][1] * 1.2

        return points

    # not finished yet
    def clear(self, button):
        for plot in self.graph.plots:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cross_section):
        self.cross_section = cross_section


class CSIApp(App):

    def build(self):
        ack = Ack_Left()
        cs = Cross_Section()
        ack.set_cross_section(cs)
        return ack

if __name__ == '__main__':
    CSIApp().run()
