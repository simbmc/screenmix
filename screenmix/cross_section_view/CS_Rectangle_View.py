'''
Created on 14.03.2016

@author: mkennert
'''

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Bezier, Line
from enaml.widgets.widget import Widget
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

'''
the class CS_Rectangle_View was developed to show the the cross section.
'''
class CS_Rectangle_View(GridLayout):
    #Constructor
    def __init__(self, *args, **kwargs):
        super(CS_Rectangle_View, self).__init__(*args, **kwargs)
        #Window.clearcolor = (1, 1, 1, 1)
        self.rectangle_height=self.height
        self.rectangle_width=self.width
        self.cs_view_height=0.5
        self.cs_view_width=0.5
        self.create_points()
        self.changeHeight(25)
        self.changeWidth(25)
        with self.canvas:
            Color(1, 1, 1)
            self.line = Line(
                    points=self.points + self.points[:2],
                    dash_length=100)

    
    '''
    the method changeHeight change the height of the cross section
    '''
    def changeHeight(self, value):
        print(value)
        self.cs_view_height=float(value)
        self.update()
    
    '''
    the method changeWidth change the height of the cross section
    '''
    def changeWidth(self,value):
        print(value)
        self.cs_view_width=float(value)
        self.update()
    
    '''
    the method create_points calculate the points of the Rectangle.
    '''
    def create_points(self):
        distance_x=10
        distance_y=20
        self.x=(self.rectangle_width+self.cs_view_width)*2.5
        self.y=(self.rectangle_height+self.cs_view_height)*3.5
        self.points=[distance_x,distance_y]
        self.points.extend([distance_x,self.y+distance_y])
        self.points.extend([self.x+distance_x,self.y+distance_y])
        self.points.extend([self.x+distance_x,distance_y])
    
    '''
    the method update make a update of the view. the method must be called if a 
    information has been changed
    '''
    def update(self):
        self.create_points()
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            self.line = Line(
                    points=self.points + self.points[:2],
                    dash_length=100)

'''
Just for testing
'''
class Main(App):
    def build(self):
        return CS_Rectangle_View()

if __name__ == '__main__':
    Main().run()