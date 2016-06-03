'''
Created on 03.06.2016

@author: mkennert
'''
from crossSectionView.aview import AView
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot


class TView(AView, GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(TView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.layers = []
    '''
    the method createGraph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def createGraph(self):
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.wmax + self.deltaX,
            ymin=0, ymax=self.hmax + self.deltaY)
        self.add_widget(self.graph)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawT()
        self.graph.add_plot(self.p)
        
    '''
    draw the double_T
    '''

    def drawT(self):
        x0 = self.graph.xmax / 2.
        y1 = 0
        x1 = x0 - self.bw / 2.
        y2 = y3 = self.bh
        x3 = x1 + self.bw / 2. - self.tw / 2.
        #y4 = y3 + self.mh
        #x5 = x3 + self.mw / 2. - self.tw / 2.
        y4 = y2 + self.th
        x5 = x3 + self.tw
        x7 = x5 - self.tw / 2. + self.bw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y2),
                (x7, y2), (x7, y1)]
    
    '''
    set the cross section
    '''

    def setCrossSection(self, crossSection):
        self.csShape = crossSection
        self.bh = self.csShape.getHeightBottom()
        self.bw = self.csShape.getWidthBottom()
        self.th = self.csShape.getHeightTop()
        self.tw = self.csShape.getWidthTop()
        self.hmax = self.csShape.getHeight()
        self.wmax = self.csShape.getWidth()
        self.createGraph()
