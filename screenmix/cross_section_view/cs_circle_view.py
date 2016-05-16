'''
Created on 01.04.2016

@author: mkennert
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout 
from numpy.random.mtrand import np

from cross_section_view.aview import AView
from kivy.garden.graph import Graph, MeshLinePlot 


class CS_Circle_View(AView, BoxLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(CS_Circle_View, self).__init__(**kwargs)
        self.cross_section_radius = 0.5
        self.layers=[1]
        self.create_graph()
        self.add_widget(self.update_all_graph)
    
    '''
    the method update_all_graph update the graph. the method should be called, when
    something has changed
    '''
    @property    
    def update_all_graph(self):
        #list = []
        '''
        for plot in self.graph.plots:
            list.append(plot)
        for layer in self.layers:
            if layer.focus:
                layer.rect = MeshLinePlot(color=[1, 0, 0, 1])
                print(layer.y_coordinate)
            else:
                layer.rect = MeshLinePlot(color=layer.colors)
            layer.rect._points = self.draw_layer(0.5)
            self.graph.add_plot(layer.rect)
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        if len(list)==0:
            self.graph._clear_buffer()
        '''
        self.draw_circle()
        self.rect = MeshLinePlot(color=[1, 0, 0, 1])
        self.rect._points=self.draw_layer(self.cross_section_radius)
        self.graph.add_plot(self.rect)
        return self.graph
    
    '''
    the method draw_layer was developed to get the _points of the rectangle
    the while_loop was create to make the rectangle set a grid.
    '''
    @staticmethod
    def draw_layer(radius):
        print('Hier')
        points=[]
        fi_outline_arr = np.linspace(0, 2 * np.pi, 60)
        points.append([np.cos(fi_outline_arr) * radius, np.sin(fi_outline_arr) * radius ])
        print(points)
        return points
    
    '''
    the method create_graph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''
    def create_graph(self):
        self.graph = Graph(
                        x_ticks_major=0.05, y_ticks_major=0.05,
                        y_grid_label=True, x_grid_label=True, padding=5,
                        xmin=0, xmax=self.cross_section_radius, ymin=0, ymax=self.cross_section_radius)
    
    def draw_circle(self):
        print('Hier')
        self.rect = MeshLinePlot(color=[1, 0, 0, 1])
        self.rect._points = self.draw_layer(0.5)
        self.graph.add_plot(self.rect)
        
        
    def set_height(self,value):
        pass
    
    def set_width(self, value):
        pass
    
    def set_percent(self, value):
        pass
    
    def add_layer(self, percent,name):
        pass
    
    def delete_layer(self):
        pass
    
    def update_layer_information(self,name,price,density,stiffness,strength,percent):
        pass
    
    '''
    Just for testing
    '''
class TestApp(App):
    def build(self):
        return CS_Circle_View()

if __name__ == '__main__':
    TestApp().run()