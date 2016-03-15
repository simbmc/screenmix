'''
Created on 15.03.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.widget import Widget
from cross_section_view.CS_Rectangle_View import CS_Rectangle_View


class Controller_View(Widget): 
    
    def __init__(self, **kwargs):
        super(Controller_View, self).__init__(**kwargs)
        self.view=CS_Rectangle_View()
    
    #def set_view(self, view):
    #    self.view=IView(view)
    
    def change_height(self,value):
        self.view.changeHeight(value)
        
    def change_width(self,value):
        self.view.changeWidth(value)
    

class ControllerAPP(App):
    def build(self):
        return Controller_View()


if __name__ == '__main__':
    ControllerAPP().run()