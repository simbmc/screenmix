'''
Created on 03.05.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from plot.filled_ellipse import FilledEllipse
from plot.line import LinePlot
from kivy.uix.popup import Popup
from material_editor.numpad import Numpad

class Multilinear(GridLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(Multilinear, self).__init__(**kwargs)
        self.cols = 2
        self.btnSize=Design.btnSize
        self.focus_btn=None
        self.create_graph()
        self.create_points(5)
        self._height=50.
        self._width=50.
        self.content_right=GridLayout(cols=2)
        self.create_information()
        
    def create_graph(self):
        self.graph = Graph(xlabel='strain', ylabel='stress',
                           x_ticks_major=10, y_ticks_major=10,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0.0, xmax=51, ymin=0, ymax=51)
        self.add_widget(self.graph)
    
    def create_points(self, n):
        self.points=[]
        self.lines=[]
        delta=100.
        self.eps_x=self.graph.xmax/delta
        self.eps_y=self.graph.ymax/delta
        counter=10
        index=self.graph.xmax/n
        while n>0:
            point=FilledEllipse(color=[255,0,0])
            point.xrange = [counter-self.eps_x,counter+self.eps_x]
            point.yrange = [counter-self.eps_y,counter+self.eps_y]
            self.points.append(point)
            self.graph.add_plot(point)
            counter+=index
            n-=1
        self.drawLines()
        
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        graph_w, graph_h = self.graph._plot_area.size  # graph size
        x_coordinate = (touch.x - x0) / graph_w*self._width
        y_coordinate = (touch.y - y0) / graph_h*self._height
        print('x: '+str(x_coordinate))
        print('y: '+str(y_coordinate))
        for point in self.points:
            if point.xrange[0]<=x_coordinate and point.xrange[1]>=x_coordinate \
                and point.yrange[0]<=y_coordinate and point.yrange[1]>=y_coordinate:
                point.color=Design.focusColor
            else:
                if point.color==Design.focusColor:
                    point.color=[255,0,0]
                    
    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        graph_w, graph_h = self.graph._plot_area.size  # graph size
        x_coordinate = (touch.x - x0) / graph_w*self._width
        y_coordinate = (touch.y - y0) / graph_h*self._height
        for i in range(len(self.points)):
            point=self.points[i]
            if point.color==Design.focusColor:
                line=self.lines[i]
                point.xrange=[x_coordinate-self.eps_x,x_coordinate+self.eps_x]
                point.yrange=[y_coordinate-self.eps_y,y_coordinate+self.eps_y]
                
    
    def create_information(self):
        self.points_lbl=Label(text='points:',size_hint_x=None, width=200)
        self.points_btn=Button(text='5',size_hint_y=None, height=self.btnSize)
        self.content_right.add_widget(self.points_lbl)
        self.content_right.add_widget(self.points_btn)
        self.height_lbl=Label(text='height:',size_hint_x=None, width=200)
        self.height_btn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.content_right.add_widget(self.height_lbl)
        self.content_right.add_widget(self.height_btn)
        self.width_lbl=Label(text='width:',size_hint_x=None, width=200)
        self.width_btn=Button(text='50',size_hint_y=None, height=self.btnSize)
        self.content_right.add_widget(self.width_lbl)
        self.content_right.add_widget(self.width_btn)
        self.add_widget(self.content_right)
    
    #not finished yet
    def drawLines(self):
        for i in range(len(self.points)):
            if i==0:
                line=LinePlot(xrange=[0., self.points[i].xrange[0]+self.eps_x],
                                    yrange=[0, self.points[i].yrange[0]+self.eps_y],
                                    color=[255,0,0])
                #line.points=[(0.,0.), (self.points[i].xrange[0]+self.eps_x,self.points[i].yrange[0]+self.eps_y)]
            else:
                line=LinePlot(xrange=[self.points[i-1].xrange[0]+self.eps_x, self.points[i].xrange[0]+self.eps_x],
                                    yrange=[self.points[i-1].yrange[0]+self.eps_y, self.points[i].yrange[0]+self.eps_y],
                                    color=[255,0,0])
            self.lines.append(line)
            self.graph.add_plot(line)
    
    '''
    create the popup with the numpad as content
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.sign_in_parent(self)
        self.popup_numpad=Popup(title='Numpad', content=self.numpad)
    
    '''
    the method finished_numpad close the numpad_popup
    '''
    def finished_numpad(self):
        self.focus_btn.text=self.numpad.textinput.text
        self.popup_numpad.dismiss()
        self.numpad.reset_text()
        #if self.focus_btn==self.
        
class TestApp(App):
        def build(self):
            return Multilinear()

TestApp().run()