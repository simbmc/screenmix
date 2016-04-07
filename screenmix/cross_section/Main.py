'''
Created on 31.03.2016

@author: mkennert
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from cross_section.Cross_Section import Cross_Section

class CSIApp(App):
    def build(self):
        layout=GridLayout(cols=2)
        csi=Cross_Section()
        layout.add_widget(csi)
        return layout

if __name__ == '__main__':
    CSIApp().run()