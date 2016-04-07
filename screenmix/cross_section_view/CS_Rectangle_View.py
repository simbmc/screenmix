'''
Created on 14.03.2016

@author: mkennert
'''


from kivy.garden.graph import Graph, MeshLinePlot 
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from itertools import cycle
from cross_section_view.AView import AView
colors = [0.8, 0.3, 0.5, 0.2, 0.1, 0.7, 0.1]
colorcycler = cycle(colors)

class Layer_Rectangle:
    # Constructor
    def __init__(self, x_coordinate, y_coordinate, height, width, colors):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self._height = height
        self._width = width
        self.rect = None
        self.colors = colors
        self.focus = False
        self.material = None
        
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''
    def mouse_within(self, x_value, y_value):
        if y_value < self.y_coordinate + self._height / 2. and y_value > self.y_coordinate - self._height / 4. and x_value > self.x_coordinate / 10. and x_value < self._width:
            return True
        else: 
            return False
    
    '''
    checked wheter the layers are the same
    '''    
    def equals(self, x, y, width, height):
        if self.x_coordinate == x and self.y_coordinate == y and self._height == height and self._width == width:
            return True
        else:
            return False
    
    '''
    the method set_height change the height of the small_keyboard-rectangle
    '''
    def set_height(self, value):
        self._height = value
    
    '''
    the method set_width change the width of the small_keyboard-rectangle
    '''
    def set_width(self, value):
        self._width = value
        
    '''
    the method set_y_coordinate change the y_coordinate of the small_keyboard-rectangle
    '''
    def set_y_coordinate(self, value):
        self.y_coordinate = value
    
    '''
    the method set_material was developed to set the small_keyboard the materials
    '''
    def set_material(self, material):
        self.material = material
    
    '''
    return the materials information
    '''
    def get_material_informations(self):
        return [self.material.name, self.material.price, self.material.density, self.material.stiffness, self.material.strength]

    
    
 

    
'''
the class CS_Rectangle_View was developed to show the the cross section,
which has a rectangle shape
'''      
class CS_Rectangle_View(BoxLayout, AView):
    # Constructor
    def __init__(self, **kwargs):
        super(CS_Rectangle_View, self).__init__(**kwargs)
        self.cross_section_height = 0.5
        self.cross_section_width = 0.25
        self.layers = []
        self.create_graph()
        self.add_widget(self.update_all_graph)
    
    '''
    the method update_all_graph update the graph. the method should be called, when
    something has changed
    '''
    @property    
    def update_all_graph(self):
        list = []
        for plot in self.graph.plots:
            list.append(plot)
        for layer in self.layers:
            if layer.focus:
                layer.rect = MeshLinePlot(color=[1, 0, 0, 1])
            else:
                layer.rect = MeshLinePlot(color=layer.colors)
            layer.rect.points = self.draw_layer(self.cross_section_width / 2, layer.y_coordinate, self.cross_section_width, layer._height)
            self.graph.add_plot(layer.rect)
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        if len(list)==0:
            self.graph._clear_buffer()
        return self.graph
        
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''
    def create_graph(self):
        self.graph = Graph(
                        x_ticks_major=0.05, y_ticks_major=0.05,
                        y_grid_label=True, x_grid_label=True, padding=5,
                        xmin=0, xmax=self.cross_section_width, ymin=0, ymax=self.cross_section_height)
    
    '''
    the method draw_layer was developed to get the points of the rectangle
    the while_loop was create to make the rectangle set a grid.
    '''
    @staticmethod
    def draw_layer(x_coordinate, y_coordinate, width, height):
        points = [(x_coordinate - width / 2., y_coordinate - height / 2.), (x_coordinate + width / 2., y_coordinate - height / 2.), (x_coordinate + width / 2., y_coordinate + height / 2.), (x_coordinate - width / 2., y_coordinate + height / 2.), (x_coordinate - width / 2., y_coordinate - height / 2.)]
        i = 0
        delta = 1000.
        distance = width / delta
        while i < delta:
            points.append((x_coordinate - width / 2. + distance, y_coordinate - height / 2.))
            points.append((x_coordinate - width / 2. + distance, y_coordinate - height / 2. + height))
            distance += width / delta
            points.append((x_coordinate - width / 2. + distance, y_coordinate - height / 2. + height))
            points.append((x_coordinate - width / 2. + distance, y_coordinate - height / 2. + height))
            i += 1
        return points
        
    '''
    the method on_touch_move is invoked after the user touch within a rectangle and move it.
    it changes the position of the rectangle
    '''
    def on_touch_move(self, touch):
        y_coordinate = (touch.y / self.graph.height) / (1 / self.cross_section_height)
        x_coordinate = (touch.x / self.graph.width) / (1 / self.cross_section_width)
        for rectangle in self.layers:
            if rectangle.focus and rectangle.mouse_within(x_coordinate, y_coordinate):
                if y_coordinate > rectangle._height / 2 and y_coordinate < self.cross_section_height - rectangle._height / 2 :
                        rectangle.rect.points = self.draw_layer(self.cross_section_width / 2, y_coordinate, self.cross_section_width, rectangle._height)
                        rectangle.set_y_coordinate(y_coordinate)
                        return
                elif y_coordinate < rectangle._height / 2:
                        rectangle.rect.points = self.draw_layer(self.cross_section_width / 2, rectangle._height / 2, self.cross_section_width, rectangle._height)
                        rectangle.set_y_coordinate(rectangle._height / 2)
                        return
                elif y_coordinate > self.cross_section_height - rectangle._height / 2:
                        rectangle.rect.points = self.draw_layer(self.cross_section_width / 2, self.cross_section_height - rectangle._height / 2, self.cross_section_width, rectangle._height)
                        rectangle.set_y_coordinate(self.cross_section_height - rectangle._height / 2)
                        return
        
    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''  
    def on_touch_down(self, touch):
        y_coordinate = (touch.y / self.graph.height) / (1 / self.cross_section_height)
        x_coordinate = (touch.x / self.graph.width) / (1 / self.cross_section_width)
        changed = False
        one_is_already_focus=False
        for rectangle in self.layers:
            if rectangle.mouse_within(x_coordinate, y_coordinate):
                if rectangle.focus == False and one_is_already_focus==False:
                    rectangle.focus = True
                    one_is_already_focus=True
                    self.cross_section.set_layer_information('Test','Test','Test','Test','Test',rectangle._height/self.cross_section_height)
                    changed = True
            else:
                if rectangle.focus == True:
                    rectangle.focus = False
                    changed = True
        if changed:
            self.update_all_graph
    
    
    # not yet so relevant. maybe we have time, we can finished it
    '''
    def collide(self,x,y,_width,_height):
        for rectangle in self.layers:
            if not rectangle.equals(x, y, _width, _height):
                #Case:1
                if y+_height/2>rectangle.y_coordinate-rectangle._height/2 and y+_height/2<rectangle.y_coordinate-rectangle._height/2:
                    print('Fall:1')
                    return rectangle._height+_height
                #Case:2
                elif y-_height/2<rectangle.y_coordinate+rectangle._height/2 and y+_height/2>rectangle.y_coordinate+rectangle._height/2:
                    print('Fall:2')
                    return -rectangle._height-_height
        return 0
    '''
    
    '''
    the method add_layer was developed to add new layer at the cross section
    '''
    def add_layer(self, value):
        height = self.cross_section_height * value
        self.layers.append(Layer_Rectangle(self.cross_section_width / 2, self.cross_section_height - height / 2., height, self.cross_section_width, [next(colorcycler), next(colorcycler), next(colorcycler), 1]))
        self.update_all_graph
    
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''
    def delete_layer(self):
        for rectangle in self.layers:
            if rectangle.focus:
                self.layers.remove(rectangle)
        self.update_all_graph
    
    def update_layer_information(self,name,price,density,stiffness,strength,percent):
        self.cross_section.set_layer_information(name,price,density,stiffness,strength,percent)
    
    #################################################################################################
    #                                Setter && Getter                                               #
    #################################################################################################
    '''
    the method set_percent change the percent shape of the selected rectangle
    ''' 
    def set_percent(self, value):
        for rectangle in self.layers:
            if rectangle.focus:
                rectangle.set_height(self.cross_section_height * value)
                self.update_all_graph
                return
    
    '''
    the method set_height change the height of the cross section shape
    and update the layers
    '''
    def set_height(self, value):
        for rectangle in self.layers:
            rectangle.set_y_coordinate(rectangle.y_coordinate / self.cross_section_height * value)
            rectangle.set_height(rectangle._height / self.cross_section_height * value)
        self.cross_section_height = value
        self.graph.ymax = self.cross_section_height
        self.update_all_graph
    
    '''
    the method set_width change the width of the cross section shape
    and update the layers
    '''
    def set_width(self, value):
        self.cross_section_width = value
        self.graph.xmax = self.cross_section_width
        for rectangle in self.layers:
            rectangle.set_width(value)
        self.update_all_graph
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_cross_section(self,cross_section):
        self.cross_section=cross_section
    
    '''
    return all layers 
    '''
    def get_layers(self):
        return self.layers