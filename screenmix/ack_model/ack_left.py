'''
Created on 12.04.2016
@author: mkennert
'''
from itertools import cycle
import random

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.garden.graph import Graph, MeshLinePlot
import numpy as np
from plot.filled_ellipse import FilledEllipse
from designClass.design import Design

class Ack_Left(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(Ack_Left, self).__init__(**kwargs)
        self.cols = 1
        self.allPlots=[]
        self.btnSize=Design.btnSize
        self.createGraph()
        self.createOptionLayout()
        self.createFocusPoint()
        self.cur_plot=None
        
    '''
    the method createGraph create the graph
    '''
    def createGraph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=0.01, ymin=0, ymax=30)
        self.add_widget(self.graph)

    '''
    the method createOptionLayout create gui-part without the graph
    '''
    def createOptionLayout(self):
        self.option_layout = GridLayout(cols=2,row_force_default=True, row_default_height=self.btnSize, size_hint_y=None, height=self.btnSize)
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
            color=[random.random(), random.random(), random.random(), 1])
        self.plot._points = self.calculatePoints()
        self.cur_plot=self.plot
        self.graph.add_plot(self.plot)
        print(self.graph.plots)

    '''
    the method alculate_points calculate the _points for 
    the graphh 
    '''

    def calculatePoints(self):
        points = [(0, 0)]
        points.append(
            (self.cs.min_of_maxstrain, self.cs.strength))
        if self.cs.view.layers:
            # calculate the second _points
            # calculate the stiffness of the reinforcement layers according to
            # mixture rule
            percent_of_layers = 0.  # the sum of the percent of the reinforcement layers
            for layer in self.cs.view.layers:
                percent_of_layers += layer.percent
            # stiffness of the section
            E_s = self.cs.strength / \
                self.cs.min_of_maxstrain
            E_r = 0.  # the stiffness of the reinforement mixture
            for layer in self.cs.view.layers:
                E_r += layer.material.stiffness * \
                    layer.percent / percent_of_layers
            # the reinforcement strain at the crack postion
            eps_r_max = self.cs.min_of_maxstrain * \
                E_s / (E_r * percent_of_layers)
            # the minimum reinforcement strain
            eps_r_min = eps_r_max - 0.6685 * \
                (1 - percent_of_layers) * self.cs.concrete_strength / \
                (percent_of_layers * E_r)
            eps_r_avg = (eps_r_max + eps_r_min) / 2.
            points.append((eps_r_avg, self.cs.strength))
            self.secondpoint=points[2]
            # calculate the third _points
            # the maximum reinforcement strain
            max_strain_r = 1e8
            for layer in self.cs.view.layers:
                cur_strain = layer.getStrain()
                max_strain_r = min(cur_strain, max_strain_r)
            # maximum composite strength
            max_strangth_c = E_r * max_strain_r * percent_of_layers
            # maximum composite strain
            max_strain_c = eps_r_avg + (max_strain_r - eps_r_max)
            points.append((max_strain_c, max_strangth_c))
            self.thirdpoint=points[-1]
        # setting the maximum of the graph
        self.graph.xmax = points[-1][0] * 1.2
        self.graph.ymax = points[-1][1] * 1.2
        self.ack.setMaxStrain(points[-1][0])
        self.graph.x_ticks_major = np.round(
            self.graph.xmax / 6., decimals=int(-np.log10(self.graph.xmax / 6)) + 1)
        self.graph.y_ticks_major = np.round(
            self.graph.ymax / 6., decimals=int(-np.log10(self.graph.ymax / 6)) + 1)
        return points

    '''
    delete all plot, except the focus plot
    '''
    def clear(self, button):
        print('clear')
        while len(self.graph.plots)>1:
            for plot in self.graph.plots:
                if not plot==self.focus and not plot==self.cur_plot:
                    self.graph.remove_plot(plot)
                    self.graph._clear_buffer()

    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''

    def setCrossSection(self, cross_section):
        self.cs = cross_section
    
    '''
    ack_left sign in by ack left
    '''
    def setAckRight(self, ack_right):
        self.ack_right=ack_right
    
    '''
    set the ack
    '''
    def setAck(self,ack):
        self.ack=ack
    
    '''
    set the position of the focuspoint.
    the point is dependet from the strainvalue 
    of ack_right
    '''
    def setFocusPosition(self, value):
        eps_x=self.graph.xmax/self.delta
        eps_y=self.graph.ymax/self.delta
        self.focus.xrange=[value-eps_x,value+eps_x]
        #calculation when the value is smaller then
        #the x-coordinate of the first point
        if value<=self.cs.min_of_maxstrain:
            #f(x)=mx => m=y1-0/x1-0
            m=self.cs.strength/self.cs.min_of_maxstrain
            self.focus.yrange=[value*m-eps_y,value*m+eps_y]
        #calculation when the value is between the  second and the third point
        elif value>self.secondpoint[0]:
            #f(x)=mx => m=y3-y2/x3-x2
            m=(self.thirdpoint[1]-self.secondpoint[1])/(self.thirdpoint[0]-self.secondpoint[0])
            #set the circle in the middle of the line
            #it's dependent from the self.graph.ymax
            if self.graph.ymax<70:
                self.focus.yrange=[value*m,value*m+2*eps_y]
            elif self.graph.ymax<100:
                self.focus.yrange=[value*m-eps_y*0.5,value*m+eps_y*1.5]
            else:
                self.focus.yrange=[value*m-eps_y,value*m+eps_y]
        #calculation when the value is between the first- and secondpoint
        else:
            #m=0 => independet from the x-value
            b=self.cs.strength
            self.focus.yrange=[-eps_y+b,+eps_y+b]
            
    '''
    create the focus point of the graph
    '''
    def createFocusPoint(self):
        self.delta=50.
        self.focus=FilledEllipse(color=[255,0,0])
        self.focus.xrange = [0,0]
        self.focus.yrange = [0,0]
        self.graph.add_plot(self.focus)
    
    '''
    update the plots
    '''
    def plotUpdate(self):
        if not self.cur_plot==None:
            self.cur_plot.color=[random.random(), random.random(), random.random(), 1]
        plot = MeshLinePlot(color=Design.focusColor)
        plot.points = self.calculatePoints()
        print('points: '+str(plot.points))
        self.cur_plot=plot
        self.allPlots.append(plot)
        self.graph.add_plot(plot)
        
    '''
    update the ack_left side
    '''
    def update(self):
        self.plotUpdate()