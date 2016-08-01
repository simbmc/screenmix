'''
Created on 27.07.2016

@author: mkennert
'''
from kivy.properties import ListProperty
from kivy.uix.button import Button
from ownComponents.design import Design


class OwnButton(Button):
    background_color_normal = Design.btnColor
    background_color_down = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        super(OwnButton, self).__init__(**kwargs)
        self.size_hint_y=None
        self.height=Design.btnHeight
        self.background_normal = ""
        self.background_down = ""
        self.background_color = self.background_color_normal
        self.color = self.background_color_down
