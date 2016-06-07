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
        print('concrete stress: '+str(concrete_stress))
        max_stress = concrete_stress
        for layer in self.concreteLayers:
            layer.xrange=[0.,concrete_stress]
            print('xrange: '+str(layer.xrange))
        # draw the stress of the reinforcing layers
        for layer in self.cs.view.layers:
            if self.ack.get_currentStrain() <= eps1:
                layer_stress = layer.material.stiffness * self.ack.get_currentStrain()
            elif self.ack.get_currentStrain() <= eps2:
                layer_stress = layer.material.stiffness * eps1
            else:
                layer_stress = layer.material.stiffness * eps1 + \
                    layer.material.stiffness * (self.ack.get_currentStrain() - eps2)
            max_stress = max(max_stress, layer_stress)
            layer.filledRectAck.xrange=[0, layer_stress]
            self.graph.add_plot(layer.filledRectAck)
        '''
        # delete the old plots
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        '''
        return self.graph
    
    def find_max_stress(self):
        self.max_stress = self.cs.concreteStiffness * \
            self.ack.get_maxStrain()
        if self.cs.view.layers:
            for layer in self.cs.view.layers:
                cur_value = layer.material.stiffness * self.ack.get_maxStrain()
                if self.max_stress < cur_value:
                    self.max_stress = cur_value
        self.graph.xmax = self.max_stress
        self.graph.x_ticks_major = int(self.max_stress / 5.)
    
    '''
    set the ack
    '''
    def set_ack(self,ack):
        self.ack=ack