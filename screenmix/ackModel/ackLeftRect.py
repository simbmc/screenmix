'''
Created on 12.04.2016
@author: mkennert
'''

from decimal import Decimal

from kivy.properties import ListProperty, StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from kivy.garden.graph import MeshLinePlot
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.filled_ellipse import FilledEllipse


class AckLeftRect(GridLayout):

    '''
    left-component of the ackrect. it shows the strain-stress-behavior 
    of the cross-section-shape rectangle by a diagram
    '''

    # cross-section-shape
    cs = ObjectProperty()
    
    ack = ObjectProperty()
    
    # right-content of the ackComponent
    ackRight = ObjectProperty()
    
    # list to save all plots
    allPlots = ListProperty([])

    # strings
    ylabelStr = StringProperty('stress [MPa]')
    
    xlabelStr = StringProperty('strain')

    # constructor
    def __init__(self, **kwargs):
        super(AckLeftRect, self).__init__(**kwargs)
        self.cols, self.btnHeight = 1, Design.btnHeight
        self.create_graph()
        self.firstPlot = True

    '''
    the method create_graph create the graph and the focus-point
    '''

    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              y_grid_label=True, x_grid_label=True,)
        self.add_widget(self.graph)
        # create the focus-point. the focus-point is a ellipse
        # you can find the class in the plot-package
        self.focus = FilledEllipse(color=[0, 0, 0])
        # set width and height of the ellipse
        self.focus.xrange, self.focus.yrange = [0, 0], [0, 0]
        self.graph.add_plot(self.focus)

    '''
    the method calculate_points calculate the points for 
    the graphh 
    '''

    def calculate_points(self):
        # the strain-stress-behavior beginning
        # always with the points (0,0)
        points = [(0, 0)]
        points.append((self.cs.minOfMaxstrain, self.cs.strength))
        if self.cs.layers:
            # calculate the second points
            # calculate the stiffness of the reinforcement layers according to
            # mixture rule
            percent_of_layers = 0.  # the sum of the p of the reinforcement layers
            for layer in self.cs.layers:
                percent_of_layers += layer.p
            # stiffness of the section
            E_s = self.cs.strength / \
                self.cs.minOfMaxstrain
            E_r = 0.  # the stiffness of the reinforement mixture
            for layer in self.cs.layers:
                E_r += layer.material.stiffness * \
                    layer.p / percent_of_layers
            # the reinforcement strain at the crack position
            eps_r_max = self.cs.minOfMaxstrain * \
                E_s / (E_r * percent_of_layers)
            # the minimum reinforcement strain
            eps_r_min = eps_r_max - 0.6685 * \
                (1 - percent_of_layers) * self.cs.concreteStrength / \
                (percent_of_layers * E_r)
            eps_r_avg = (eps_r_max + eps_r_min) / 2.
            points.append((eps_r_avg, self.cs.strength))
            self.secondpoint = points[2]
            # calculate the third points
            # the maximum reinforcement strain
            max_strain_r = 1e8
            for layer in self.cs.layers:
                cur_strain = layer.strain
                max_strain_r = min(cur_strain, max_strain_r)
            # maximum composite strength
            max_strangth_c = E_r * max_strain_r * percent_of_layers
            # two small reinforcement ratio, no mulitplecracking
            if max_strangth_c < self.cs.strength:
                points.pop()
            else:  # multiple cracking
                # maximum composite strain
                max_strain_c = eps_r_avg + (max_strain_r - eps_r_max)
                points.append((max_strain_c, max_strangth_c))
                self.thirdpoint = points[-1]
        self.ack.sliderStrain.max = points[-1][0]
        return points
    
    '''
    update the graph-borders
    '''
   
    def update_graph_border(self):
        # cur minimum/maximum
        minM, maxM = 1e10, -1e10  # x-values
        minN, maxN = 1e10, -1e10  # y-values
        # find the min and max values
        for plt in self.graph.plots:
                for p in plt.points:
                    x, y = p[0], p[1]
                    if x > maxM:
                        maxM = x
                    if x < minM:
                        minM = x
                    if y > maxN:
                        maxN = y
                    if y < minN:
                        minN = y
        eps = 1.05
        # update the graph-borders
        self.graph.xmin = float(minM) * eps
        self.graph.xmax = float(maxM) * eps
        self.graph.ymin = float(minN) * eps
        self.graph.ymax = float(maxN) * eps
        self.graph.y_ticks_major = float(
            format((self.graph.ymax - self.graph.ymin) / 5., '.1g'))
        self.graph.x_ticks_major = float(
            format((self.graph.xmax - self.graph.xmin) / 5., '.1g'))
        # update the circle size
        eps_x = self.graph.xmax / Design.deltaCircle
        eps_y = self.graph.ymax / Design.deltaCircle
        self.focus.xrange = [ -eps_x, eps_x]
        self.focus.yrange = [ -eps_y, eps_y]
        self.ack.sliderStrain.value = 0
        
    '''
    set the position of the focuspoint.
    the point is dependet from the strainvalue of ackRight
    '''

    def move_position(self, value):
        eps_x = self.graph.xmax / Design.deltaCircle
        eps_y = self.graph.ymax / Design.deltaCircle
        self.focus.xrange = [value - eps_x, value + eps_x]
        # calculation when the value is smaller then
        # the x-coordinate of the first point
        if value <= self.cs.minOfMaxstrain:
            # f(x)=mx => m=y1-0/x1-0
            m = self.cs.strength / self.cs.minOfMaxstrain
            self.focus.yrange = [value * m - eps_y, value * m + eps_y]
            self.ack.lblStress.text = self.ack.stressStr + str('%.2E' % Decimal(str(value * m)))
        # calculation when the value is between the  second and the third point
        elif value > self.secondpoint[0]:
            # f(x)=mx => m=y3-y2/x3-x2
            m = (self.thirdpoint[1] - self.secondpoint[1]) / \
                (self.thirdpoint[0] - self.secondpoint[0])
            b = self.secondpoint[1] - m * self.secondpoint[0]
            y = value * m + b
            # set the circle in the middle of the line
            # it's dependent from the self.graph.ymax
            self.focus.yrange = [y - eps_y, y + eps_y]
            self.ack.lblStress.text = self.ack.stressStr + str('%.2E' % Decimal(str(y)))
        # calculation when the value is between the first- and secondpoint
        else:
            # m=0 => independet from the x-value
            b = self.cs.strength
            self.focus.yrange = [b - eps_y, b + eps_y]
            self.ack.lblStress.text = self.ack.stressStr + str('%.2E' % Decimal(str(b)))

    '''
    update the plot
    '''

    def update(self):
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot.points = self.calculate_points()
        # safe the cur-plot for the delete-method
        if self.firstPlot:
            self.curPlot = self.plot
            self.firstPlot = False
        else:
            # set the color of the old-focus-plot to black
            self.curPlot.color = [0, 0, 0, 1]
            self.curPlot = self.plot
        # safe the plot in the allplot list. it's necessary for the update
        self.allPlots.append(self.plot)
        self.graph.add_plot(self.plot)
        self.update_graph_border()
