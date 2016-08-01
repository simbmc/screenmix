'''
Created on 27.07.2016

@author: mkennert
'''
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from ownComponents.design import Design


class OwnPopup(Popup):
    background_color_normal = Design.foregroundColor
    def __init__(self, **kwargs):
        super(OwnPopup, self).__init__(**kwargs)
        self.background='(1,1,1,1)'
        self.title_color=self.background_color_normal
