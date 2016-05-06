'''
Created on 06.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot

class MultilinearView(GridLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(MultilinearView, self).__init__(**kwargs)
        self.cols = 1
        self.create_graph()
        self.create_points(5)
    
    '''
    create the graph of the view
    '''
    def create_graph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=10, y_ticks_major=10,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=51, ymin=0, ymax=51)
        self.add_widget(self.graph)
    
    '''
    create the points 
    '''
    def create_points(self, n):
        self._points=[]
        self.lines=[]
        delta=100.
        self.eps_x=self.graph.xmax/delta
        self.eps_y=self.graph.ymax/delta
        counter=(self.graph.xmax-2)/n
        index=self.graph.xmax/n
        while n>0:
            point=FilledEllipse(color=[255,0,0])
            point.xrange = [counter-self.eps_x,counter+self.eps_x]
            point.yrange = [counter-self.eps_y,counter+self.eps_y]
            self._points.append(point)
            self.graph.add_plot(point)
            counter+=index
            n-=1
        self.drawLines()
    
    '''
    reaction when the user move touch on the graph 
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        graph_w, graph_h = self.graph._plot_area.size  # graph size
        x_coordinate = (touch.x - x0) / graph_w*self.editor._width
        y_coordinate = (touch.y - y0) / graph_h*self.editor._height
        print('x: '+str(x_coordinate))
        print('y: '+str(y_coordinate))
        for point in self._points:
            if point.xrange[0]<=x_coordinate and point.xrange[1]>=x_coordinate \
                and point.yrange[0]<=y_coordinate and point.yrange[1]>=y_coordinate:
                point.color=Design.focusColor
            else:
                if point.color==Design.focusColor:
                    point.color=[255,0,0]
    
    '''
    reaction when the user move over the graph
    '''             
    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        graph_w, graph_h = self.graph._plot_area.size  # graph size
        x_coordinate = (touch.x - x0) / graph_w*self.editor._width
        y_coordinate = (touch.y - y0) / graph_h*self.editor._height
        for i in range(len(self._points)):
            point=self._points[i]
            if point.color==Design.focusColor:
                line=self.lines[i]
                point.xrange=[x_coordinate-self.eps_x,x_coordinate+self.eps_x]
                point.yrange=[y_coordinate-self.eps_y,y_coordinate+self.eps_y]
    
    #not finished yet
    def drawLines(self):
        for i in range(len(self._points)):
            if i==0:
                line=LinePlot(xrange=[0., self._points[i].xrange[0]+self.eps_x],
                                    yrange=[0, self._points[i].yrange[0]+self.eps_y],
                                    color=[255,0,0])
                #line._points=[(0.,0.), (self._points[i].xrange[0]+self.eps_x,self._points[i].yrange[0]+self.eps_y)]
            else:
                line=LinePlot(xrange=[self._points[i-1].xrange[0]+self.eps_x, self._points[i].xrange[0]+self.eps_x],
                                    yrange=[self._points[i-1].yrange[0]+self.eps_y, self._points[i].yrange[0]+self.eps_y],
                                    color=[255,0,0])
            self.lines.append(line)
            self.graph.add_plot(line)
    
    '''
    update the width of the graph
    '''
    def updateWidth(self):
        self.graph.xmax=self.editor.getWidth()
    
    '''
    update the height of the graph
    '''
    def updateHeight(self):
        self.graph.ymax=self.editor.getHeight()
    
    '''
    update the number of points
    '''
    def updatePoints(self):
        #clear all points and lines
        while len(self.graph.plots)>0:
            for plot in self.graph.plots:
                self.graph.remove_plot(plot)
                self.graph._clear_buffer()
        #draw the new points and lines
        self.create_points(self.editor.getPoints())
        self.drawLines()
    
    '''
    sign in by the parent
    '''
    def sign_in(self, parent):
        self.editor=parent