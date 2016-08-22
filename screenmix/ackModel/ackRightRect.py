'''
Created on 14.04.2016
@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout

from ownComponents.ownGraph import OwnGraph
from plot.filled_rect import FilledRect


class AckRightRect(GridLayout):

    '''
    right-component of the ack-rect. this component show the 
    stress-behavior of the single layers and the matrix
    '''

    # important components
    cs = ObjectProperty()
    ack, ackLeft = ObjectProperty(), ObjectProperty()

    # strings
    xlabelStr = StringProperty('stress [MPa]')  # string-xlabel of the graph
    ylabelStr = StringProperty('height [m]')  # string-ylabel of the graph

    # constructor
    def __init__(self, **kwargs):
        super(AckRightRect, self).__init__(**kwargs)
        self.cols = 1

    '''
    the method create_graph create the graph. the graph shows
    the strain behaviour of the layers
    '''

    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              y_grid_label=True, x_grid_label=True)
        self.add_widget(self.graph)

    '''
    update the layerinformation of layers
    '''

    def update(self):
        # update the height of the cs
        self.graph.ymax = self.cs.h
        self.graph.y_ticks_major = self.cs.h / 5.
        self.find_max_stress()
        # remove all plots from the graph
        for plot in self.graph.plots:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        self.concreteLayers = []  # reset the concreteLayers
        # get the places where are no layer
        free_places = self.cs.view.get_free_places()
        # create the filled-rects of the free-places
        for layer in free_places:
            filledRect = FilledRect(xrange=[0., 1e-10],
                                    yrange=[layer[0], layer[1]],
                                    color=[255, 255, 255])
            self.concreteLayers.append(filledRect)
            # add the filled-graphs to the graph
            self.graph.add_plot(filledRect)
        self.update_plots()

    '''
    update the plots
    '''

    def update_plots(self):
        # the four points determining the ACK curve
        points = self.ackLeft.calculate_points()
        if len(points) == 4:  # multiple cracking
            eps1, eps2 = points[1][0], points[2][0]
        else:  # no layers exist
            eps1 = points[1][0] * self.maxStress * 1e4
            self.graph.xmax = eps1
            self.graph.x_ticks_major = eps1 / 5.
        # draw the free places of the cross section
        concrete_stress = self.cs.concreteStiffness * \
            self.ack.sliderStrain.value * \
            (self.ack.sliderStrain.value <= eps1)
        max_stress = concrete_stress
        for layer in self.concreteLayers:
            layer.xrange = [0., concrete_stress]
        # draw the stress of the reinforcing layers
        for layer in self.cs.layers:
            # if the cross section has layers and the strain is smaller
            # as the cracking stress show just a part of the graph because then
            # the user can see the behavior of the concrete
            if self.ack.sliderStrain.value <= eps1:
                if not len(self.cs.layers) == 0:
                    self.find_max_stiffness()
                    self.graph.xmax = self.maxStiffness * points[1][0]
                    self.graph.x_ticks_major = int(self.graph.xmax / 5.)
                layer_stress = layer.material.stiffness * \
                    self.ack.sliderStrain.value
            # cracking-process
            elif self.ack.sliderStrain.value <= eps2:
                layer_stress = layer.material.stiffness * eps1
                self.graph.xmax = self.maxStress
                self.graph.x_ticks_major = int(self.graph.xmax / 5.)
            # leaf the cracking-process
            else:
                layer_stress = layer.material.stiffness * eps1 + \
                    layer.material.stiffness * \
                    (self.ack.sliderStrain.value - eps2)
                self.graph.xmax = self.maxStress
                self.graph.x_ticks_major = int(self.graph.xmax / 5.)
            max_stress = max(max_stress, layer_stress)
            layer.layerAck.xrange = [0, layer_stress]
            self.graph.add_plot(layer.layerAck)
        self.graph.y_ticks_major = self.graph.ymax / 5.
        return self.graph

    '''
    find the max stress of the layers
    '''

    def find_max_stress(self):
        # first max-stress
        self.maxStress = self.cs.concreteStiffness * self.ack.sliderStrain.max
        # if the cross-section contains layers
        if not len(self.cs.layers) == 0:
            self.find_max_stiffness()
            cur = self.maxStiffness * self.ack.sliderStrain.max
            if cur > self.maxStress:
                self.maxStress = cur
        self.graph.x_ticks_major = int(self.maxStress / 5.)

    '''
    find the max-stiffness of the layers
    '''

    def find_max_stiffness(self):
        stiffness = 0.  # cur infinimum
        for layer in self.cs.layers:
            if layer.material.stiffness > stiffness:
                stiffness = layer.material.stiffness
        self.maxStiffness = stiffness
