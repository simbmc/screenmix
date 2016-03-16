'''
Created on 14.03.2016

@author: mkennert
'''

'''
the class CS_Rectangle_View was developed to show the the cross section.
'''

from enaml.widgets.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Bezier, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class CS_Rectangle_View(GridLayout):
    #Constructor
    
    def __init__(self, *args, **kwargs):
        super(CS_Rectangle_View, self).__init__(*args, **kwargs)
        #Window.clearcolor = (1, 1, 1, 1)
        self.rectangle_height=self.height
        self.rectangle_width=self.width
        self.cs_view_height=0.5
        self.cs_view_width=0.5
        self.material_points=None
        self.create_points()
        self.change_height(25)
        self.change_width(25)
        
    
    '''
    the method change_height change the height of the cross section
    '''
    def change_height(self, value):
        print(value)
        self.cs_view_height=float(value)
        self.update()
    
    '''
    the method change_width change the height of the cross section
    '''
    def change_width(self,value):
        print(value)
        self.cs_view_width=float(value)
        self.update()
    
    '''
    the method create_points calculate the points of the Rectangle.
    '''
    def create_points(self):
        self.distance_x=10
        self.distance_y=20
        self.x=(self.rectangle_width+self.cs_view_width)*2.5
        self.y=(self.rectangle_height+self.cs_view_height)*3.5
        self.points=[self.distance_x,self.distance_y]
        self.points.extend([self.distance_x,self.y+self.distance_y])
        self.points.extend([self.x+self.distance_x,self.y+self.distance_y])
        self.points.extend([self.x+self.distance_x,self.distance_y])
    
    '''
    the method update make a update of the view. the method must be called if a 
    information has been changed
    '''
    def update(self):
        self.create_points()
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            Line(
                    points=self.points + self.points[:2]
                )
            '''
            if self.material_points!=None:
                for x in xrange(len(self.material_points)):
                    Line(
                         points=self.material_points[x],
                         width=3
                         )
            '''
    '''
    not finished yet
    '''
    def add(self, percent):
        if self.material_points==None:
            points=[self.distance_x,self.distance_y]
            points.append([self.distance_x,self.distance_y+self.y*percent])
            points.append([self.x+self.distance_x,self.distance_y+self.y*percent])
            points.append([self.x+self.distance_x,self.distance_y])
            self.material_points=points
        self.update()   
