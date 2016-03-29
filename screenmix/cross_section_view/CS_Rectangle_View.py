'''
Created on 14.03.2016

@author: mkennert
'''

'''
the class CS_Rectangle_View was developed to show the the cross section.
'''
from kivy.garden.graph import Graph, MeshLinePlot 
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from itertools import cycle
colors = [0.2,0.4,0.8,0.2,0.1,0.7,0.1]
colorcycler = cycle(colors)
class Layer:
    #Constructor
    def __init__(self,x_coordinate,y_coordinate,height, width, colors):#,name,price,density,stiffness,stength,percent):
        self.x_coordinate=x_coordinate
        self.y_coordinate=y_coordinate
        self._height=height
        self._width=width
        self.rect=None
        self.colors=colors
        self.focus=False
        '''
        self.name=name
        self.price=price
        self.density=density
        self.stiffness=stiffness
        self.strength=strength
        self.percent=percent
        '''
        
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''
    def mouse_within(self,x_value, y_value):
        if y_value<self.y_coordinate+self._height/2. and y_value>self.y_coordinate-self._height/4. and x_value>self.x_coordinate/10. and x_value<self._width:
            return True
        else: 
            return False
    '''
    checked wheter the rectangles are the same
    '''    
    def equals(self,x,y,width,height):
        if self.x_coordinate==x and self.y_coordinate==y and self._height==height and self._width==width:
            return True
        else:
            return False
    
    def change_height(self,value):
        self._height=value
    
    
    def change_width(self,value):
        self._width=value
        
    
    def change_y_coordinate(self,value):
        self.y_coordinate=value
    
        
    
class CS_Rectangle_View(BoxLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(CS_Rectangle_View, self).__init__(**kwargs)
        self.cross_section_height=0.5
        self.cross_section_width=0.25
        self.rectangle_1=Layer(self.cross_section_width/2,0.1,0.05,self.cross_section_width,[next(colorcycler), next(colorcycler), next(colorcycler), 1])
        self.rectangle_2=Layer(self.cross_section_width/2,0.2,0.1,self.cross_section_width,[next(colorcycler), next(colorcycler), next(colorcycler), 1])
        self.rectangle_3=Layer(self.cross_section_width/2,0.4,0.05,self.cross_section_width,[next(colorcycler), next(colorcycler), next(colorcycler), 1])
        self.rectangle_4=Layer(self.cross_section_width/2,0.3,0.05,self.cross_section_width,[next(colorcycler), next(colorcycler), next(colorcycler), 1])
        self.rectangles=[self.rectangle_1,self.rectangle_3, self.rectangle_2,self.rectangle_4]
        #self.rectangles=[]
        self.create_graph()
        self.add_widget(self.update_all_graph)
    '''
    the method update_all_graph update the graph. the method should be called, when
    something has changed
    '''
    @property    
    def update_all_graph(self):
        list=[]
        for plot in self.graph.plots:
            list.append(plot)
        for rectangle in self.rectangles:
            if rectangle.focus:
                rectangle.rect = MeshLinePlot(color=[1,0,0,1])
            else:
                rectangle.rect = MeshLinePlot(color=rectangle.colors)
            rectangle.rect.points = self.draw_rect(self.cross_section_width/2, rectangle.y_coordinate, self.cross_section_width, rectangle._height)
            self.graph.add_plot(rectangle.rect)
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        return self.graph
        
    
        
    '''
    the method create_graph create the graph, where you can add 
    the rectangles. the method should be called only once at the beginning
    '''
    def create_graph(self):
        self.graph = Graph(
                        x_ticks_major=0.05, y_ticks_major=0.05, 
                        y_grid_label=True, x_grid_label=True, padding=5, 
                        xmin=0, xmax=self.cross_section_width, ymin=0, ymax=self.cross_section_height)
    
    
    def change_height(self, value):
        for rectangle in self.rectangles:
            rectangle.change_y_coordinate(rectangle.y_coordinate/self.cross_section_height*value)
            rectangle.change_height(rectangle._height/self.cross_section_height*value)
        self.cross_section_height=value
        self.graph.ymax=self.cross_section_height
        self.update_all_graph
    
    def change_width(self, value):
        print('Width: '+str(value))
        self.cross_section_width=value
        self.graph.xmax=self.cross_section_width
        for rectangle in self.rectangles:
            rectangle.change_width(value)
        self.update_all_graph
    
    '''
    the method draw_rect was developed to get the points of the rectangle
    the while_loop was create to make the rectangle set a grid.
    '''
    @staticmethod
    def draw_rect(x_coordinate, y_coordinate, width, height):
        points=[(x_coordinate - width / 2., y_coordinate - height / 2.), (x_coordinate + width / 2., y_coordinate - height / 2.), (x_coordinate + width / 2., y_coordinate + height / 2.), (x_coordinate - width / 2., y_coordinate + height / 2.), (x_coordinate - width / 2., y_coordinate - height / 2.)]
        i=0
        delta=1000.
        distance=width/delta
        while i<delta:
            points.append((x_coordinate - width / 2.+distance, y_coordinate - height / 2.))
            points.append((x_coordinate - width / 2.+distance, y_coordinate - height / 2.+height))
            distance+=width/delta
            points.append((x_coordinate - width / 2.+distance, y_coordinate - height / 2.+height))
            points.append((x_coordinate - width / 2.+distance, y_coordinate - height / 2.+height))
            i+=1
        return points
        
    '''
    the method on_touch_move is invoked when the user touch within a rectangle and move it.
    it change the position of the rectangle
    '''
    def on_touch_move(self, touch):
        y_coordinate=(touch.y/self.graph.height)/(1/self.cross_section_height)
        x_coordinate=(touch.x/self.graph.width)/(1/self.cross_section_width)
        for rectangle in self.rectangles:
            if rectangle.mouse_within(x_coordinate,y_coordinate):
                if y_coordinate > rectangle._height/2 and y_coordinate < self.cross_section_height-rectangle._height/2 :
                        rectangle.rect.points = self.draw_rect(self.cross_section_width/2, y_coordinate, self.cross_section_width,rectangle._height)
                        rectangle.change_y_coordinate(y_coordinate)
                        return
                elif y_coordinate < rectangle._height/2:
                        rectangle.rect.points = self.draw_rect(self.cross_section_width/2, rectangle._height/2, self.cross_section_width,rectangle._height)
                        rectangle.change_y_coordinate(rectangle._height/2)
                        return
                elif y_coordinate > self.cross_section_height-rectangle._height/2:
                        rectangle.rect.points = self.draw_rect(self.cross_section_width/2, self.cross_section_height-rectangle._height/2, self.cross_section_width, rectangle._height)
                        rectangle.change_y_coordinate(self.cross_section_height-rectangle._height/2)
                        return
        
         
    def on_touch_down(self, touch):
        y_coordinate=(touch.y/self.graph.height)/(1/self.cross_section_height)
        x_coordinate=(touch.x/self.graph.width)/(1/self.cross_section_width)
        changed=False
        for rectangle in self.rectangles:
            if rectangle.mouse_within(x_coordinate,y_coordinate):
                if rectangle.focus==False:
                    rectangle.focus=True
                    changed=True
            else:
                if rectangle.focus==True:
                    rectangle.focus=False
                    changed=True
        if changed:
            self.update_all_graph
    
    
    #not yet so revelant. maybe we have time, we can finished it
    '''
    def collide(self,x,y,_width,_height):
        for rectangle in self.rectangles:
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
    def add_layer(self,rectangle):
        self.rectangles.append(Layer(rectangle))
        self.update_all_graph
    
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''
    def delete_layer(self):
        for rectangle in self.rectangles:
            if rectangle.focus:
                self.rectangles.remove(rectangle)
        self.update_all_graph
    
    def change_percent(self,value):
        for rectangle in self.rectangles:
            if rectangle.focus:
                rectangle.change_height(value)
                self.update_all_graph
                return
    
'''
Just for testing
'''
class TestApp(App):
    def build(self):
        return CS_Rectangle_View()

if __name__ == '__main__':
    TestApp().run()