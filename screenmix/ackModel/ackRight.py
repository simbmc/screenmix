'''
Created on 14.04.2016
@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_rect import FilledRect


class AckRight(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(AckRight, self).__init__(**kwargs)
        self.cols = 1
    
    '''
    create the gui of the ack_right
    '''
    def create_gui(self):
        self.create_graph()
        self.update()

    '''
    the method create_graph create the graph
    '''

    def create_graph(self):
        self.graph = Graph(xlabel='stress [MPa]', ylabel='height [m]',
                           y_ticks_major=0.1,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=0.0005, ymin=0, ymax=self.cs.h)
        self.add_widget(self.graph)
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.create_gui()

    '''
    ackLeft sign in by ack right
    '''

    def set_ack_left(self, ack_left):
        self.ackLeft = ack_left

    '''
    update the layerinformation of layers
    '''
    def update(self):
        self.graph.ymax=self.cs.h
        self.find_max_stress()
        for plot in self.graph.plots:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        self.concreteLayers=[]
        free_places = self.cs.view.get_free_places()
        for layer in free_places:
            filledRect = FilledRect(xrange=[0., 1e-5],
                                   yrange=[layer[0], layer[1]],
                                   color=[255, 255, 255])
            self.concreteLayers.append(filledRect)
            self.graph.add_plot(filledRect)
        self.update_plots()
    
    '''
    update the plots
    '''
    def update_plots(self):
        # the four points determining the ACK curve
        if self.cs.view.layers:  # reinforcement layer exists
            points = self.ackLeft.calculate_points()
            eps1, eps2, eps3 = points[1][0], points[2][0], points[3][0]
        else:
            eps1, eps2 = 1e6, 1e6
        # draw the free places of the cross section
        concrete_stress = self.cs.concreteStiffness * \
            self.ack.get_currentStrain() * (self.ack.get_currentStrain() <= eps1)
        max_stress = concrete_stress
        for layer in self.concreteLayers:
            layer.xrange=[0.,concrete_stress]
        # draw the stress of the reinforcing layers
        for layer in self.cs.view.layers:
            if self.ack.get_currentStrain() <= eps1:
                if not len(self.cs.view.layers)==0:
                    self.find_max_stiffness()
                    self.graph.xmax = self.maxStiffness*points[1][0]  
                    self.graph.x_ticks_major = int(self.graph.xmax/10.)
                layer_stress = layer.material.stiffness * self.ack.get_currentStrain()
            elif self.ack.get_currentStrain() <= eps2:
                layer_stress = layer.material.stiffness * eps1
                self.graph.xmax = self.max_stress
                self.graph.x_ticks_major = int(self.graph.xmax / 5.)
            else:
                layer_stress = layer.material.stiffness * eps1 + \
                    layer.material.stiffness * (self.ack.get_currentStrain() - eps2)
                self.graph.xmax = self.max_stress
                self.graph.x_ticks_major = int(self.graph.xmax / 5.)
            max_stress = max(max_stress, layer_stress)
            layer.layerAck.xrange=[0, layer_stress]
            self.graph.add_plot(layer.layerAck)
        return self.graph
    
    '''
    find the max stress of the layers
    '''
    def find_max_stress(self):
        self.max_stress = self.cs.concreteStiffness * \
            self.ack.get_maxStrain()
        if not len(self.cs.view.layers)==0:
            self.find_max_stiffness()
            cur=self.maxStiffness*self.ack.get_maxStrain()
            if cur>self.max_stress:
                self.max_stress=cur
        self.graph.x_ticks_major = int(self.max_stress / 5.)
    
    '''
    find the max stiffness
    '''
    def find_max_stiffness(self):
        stiffness=0.
        for layer in self.cs.view.layers:
            if layer.material.stiffness>stiffness:
                stiffness=layer.material.stiffness
        self.maxStiffness=stiffness
            
    '''
    set the ack
    '''
    def set_ack(self,ack):
        self.ack=ack