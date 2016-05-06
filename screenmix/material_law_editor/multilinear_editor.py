'''
Created on 03.05.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from kivy.garden.graph import Graph, MeshLinePlot
from material_law_editor.mulitlinearInformation import MultilinearInformation
from material_law_editor.multilinear_view import MultilinearView


class Multilinear(GridLayout):
    #constructor
    def __init__(self, **kwargs):
        super(Multilinear, self).__init__(**kwargs)
        self.cols = 2
        self._height=50.
        self._width=50.
        self._points=5
        self.information=MultilinearInformation()
        self.view=MultilinearView()
        self.information.sign_in(self)
        self.view.sign_in(self)
        self.add_widget(self.view)
        self.add_widget(self.information)
    
    '''
    set the width of the graph
    '''
    def setWidth(self, value):
        self._width=value
        self.view.updateWidth()
    
    '''
    set the height of the graph
    '''
    def setHeight(self,value):
        self._height=value
        self.view.updateHeight()
    
    '''
    return the height of the graph
    '''
    def getHeight(self):
        return self._height
    
    '''
    return the width of the graph
    '''
    def getWidth(self):
        return self._width
    
    '''
    set the numbers of points which the graph should have
    '''
    def setPoints(self,value):
        self._points=value
        self.view.updatePoints()
    
    '''
    return the number of points
    '''
    def getPoints(self):
        return self._points     

'''
Just for testing
'''
class TestApp(App):
        def build(self):
            return Multilinear()

TestApp().run()