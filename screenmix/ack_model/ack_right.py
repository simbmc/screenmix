'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_rect import FilledRect


class Ack_Right(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(Ack_Right, self).__init__(**kwargs)
        self.cols = 1
    
    '''
    create the gui of the ack_right
    '''
    def createGui(self):
        self.createGraph()
        self.update()

    '''
    the method createGraph create the graph
    '''

    def createGraph(self):
        self.graph = Graph(xlabel='stress [MPa]', ylabel='height [m]',
                           y_ticks_major=0.1,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=0.0005, ymin=0, ymax=self.cs.cheight)
        self.add_widget(self.graph)
    
    
    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''

    def setCrossSection(self, cross_section):
        self.cs = cross_section
        self.createGui()

    '''
    ack_left sign in by ack right
    '''

    def setAckLeft(self, ack_left):
        self.ack_left = ack_left

    '''
    update the layerinformation of layers
    '''
    '''
    def update(self):

        # the four points determining the ACK curve
        if self.cs.view.layers:  # reinforcement layer exists
            points = self.ack_left.calculatePoints()
            eps1, eps2, eps3 = points[1][0], points[2][0], points[3][0]

        else:
            eps1, eps2 = 1e6, 1e6

        list = []
        for plot in self.graph.plots:
            list.append(plot)
        # draw the free places of the cross section
        concrete_stress = self.cs.concrete_stiffness * \
            self.ack.getCurrentStrain() * (self.ack.getCurrentStrain() <= eps1)
        max_stress = concrete_stress
        free_places = self.cs.view.getFreePlaces()
        for layer in free_places:
            self.rect = FilledRect(xrange=[0., concrete_stress],
                                   yrange=[layer[0], layer[1]],
                                   color=[255, 255, 255])
            self.graph.add_plot(self.rect)
        # draw the stress of the reinforcing layers
        for layer in self.cs.view.layers:
            if self.ack.getCurrentStrain() <= eps1:
                layer_stress = layer.material.stiffness * self.ack.getCurrentStrain()
            elif self.ack.getCurrentStrain() <= eps2:
                layer_stress = layer.material.stiffness * eps1
            else:
                layer_stress = layer.material.stiffness * eps1 + \
                    layer.material.stiffness * (self.ack.getCurrentStrain() - eps2)
            max_stress = max(max_stress, layer_stress)
            layer.rect = FilledRect(xrange=[0, layer_stress],
                                    yrange=[
                                        layer.y_coordinate - layer._height / 2., layer.y_coordinate + layer._height / 2.],
                                    color=layer.colors)
            self.graph.add_plot(layer.rect)

        # change the x-aixs limit
        #self.graph.xmax = max_stress
        #self.graph.x_ticks_major = int(max_stress / 5.)
        self.findMaxStress()
        # delete the old plots
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        return self.graph
    '''
    def update(self):
        self.graph.ymax=self.cs.cheight
        self.findMaxStress()
        for plot in self.graph.plots:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        self.concreteLayers=[]
        free_places = self.cs.view.getFreePlaces()
        for layer in free_places:
            filledRect = FilledRect(xrange=[0., 1e-5],
                                   yrange=[layer[0], layer[1]],
                                   color=[255, 255, 255])
            self.concreteLayers.append(filledRect)
            self.graph.add_plot(filledRect)
        self.updatePlots()
    
    
    def updatePlots(self):
        # the four points determining the ACK curve
        if self.cs.view.layers:  # reinforcement layer exists
            points = self.ack_left.calculatePoints()
            eps1, eps2, eps3 = points[1][0], points[2][0], points[3][0]

        else:
            eps1, eps2 = 1e6, 1e6
        # draw the free places of the cross section
        concrete_stress = self.cs.concrete_stiffness * \
            self.ack.getCurrentStrain() * (self.ack.getCurrentStrain() <= eps1)
        print('concrete stress: '+str(concrete_stress))
        max_stress = concrete_stress
        for layer in self.concreteLayers:
            layer.xrange=[0.,concrete_stress]
            print('xrange: '+str(layer.xrange))
        # draw the stress of the reinforcing layers
        for layer in self.cs.view.layers:
            if self.ack.getCurrentStrain() <= eps1:
                layer_stress = layer.material.stiffness * self.ack.getCurrentStrain()
            elif self.ack.getCurrentStrain() <= eps2:
                layer_stress = layer.material.stiffness * eps1
            else:
                layer_stress = layer.material.stiffness * eps1 + \
                    layer.material.stiffness * (self.ack.getCurrentStrain() - eps2)
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
    
    def findMaxStress(self):
        self.max_stress = self.cs.concrete_stiffness * \
            self.ack.getMaxStrain()
        if self.cs.view.layers:
            for layer in self.cs.view.layers:
                cur_value = layer.material.stiffness * self.ack.getMaxStrain()
                if self.max_stress < cur_value:
                    self.max_stress = cur_value
        self.graph.xmax = self.max_stress
        self.graph.x_ticks_major = int(self.max_stress / 5.)
    
    '''
    set the ack
    '''
    def setAck(self,ack):
        self.ack=ack