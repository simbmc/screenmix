'''
Created on 26.07.2016

@author: mkennert
'''
__version__ = '1.0'
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar, ActionPrevious
from kivy.uix.gridlayout import GridLayout

from ackModel.ack import Ack
from crossSection.crossSection import CrossSection
from materialEditor.editor import Material_Editor
from ownComponents.design import Design
from kivy.properties import BooleanProperty

Window.clearcolor = (1, 1, 1, 1)
'''
create the ActionBar in the mainMenu with the kv.file screenmixapp
'''
class AppActionBar(ActionBar):
    pass

'''
create the ActionMenu in the mainMenu with the kv.file screenmixapp
'''
class ActionMenu(ActionPrevious):
    pass

class ScreenmixApp(App):
    
    # switch to proof whether the ack has been created
    boolACK = BooleanProperty(True)
    
    # switch to proof whether the material-editor has been created
    boolME = BooleanProperty(True)
    
    '''
    Build the application
    '''
    
    def build(self):
        bar = AppActionBar()
        self.content = GridLayout(cols=1, spacing=Design.spacing)
        self.content.add_widget(bar)
        self.cs = CrossSection()
        self.content.add_widget(self.cs)
        # Cross Section is the default view
        self.contentLayout = self.cs
        return self.content

    '''
    create the ask_view
    '''

    def create_ack_view(self):
        self.ack= Ack()
        self.cs.shapeRectangle.ack = self.ack.ackRect
        self.ack.ackRect.cs = self.cs.shapeRectangle
        self.ack.ackRect.create_gui()
        # when you add more shapes, make sure that the
        # shapes has a ownAck

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = Material_Editor()
        self.materialEditor.set_cross_section(self.cs)

    ##########################################################################
    # Attention:When you want write a new show-method than you must make sure    #
    # that actually component is remove from the widget and set                  #
    # the contentLayout to the showed component                                  #
    ##########################################################################

    '''
    show the ack-view
    '''

    def show_ack_view(self):
        if self.boolACK:
            self.create_ack_view()
            self.boolACK=False
        self.ack.content.update()
        self.content.remove_widget(self.contentLayout)
        self.content.add_widget(self.ack)
        self.contentLayout = self.ack

    '''
    show the cross section view
    '''

    def show_cross_section_view(self):
        self.content.remove_widget(self.contentLayout)
        self.content.add_widget(self.cs)
        self.contentLayout = self.cs

    '''
    show the material-editor
    '''

    def show_material_editor(self):
        if self.boolME:
            self.create_material_editor()
            self.boolME=False
        self.content.remove_widget(self.contentLayout)
        self.content.add_widget(self.materialEditor)
        self.contentLayout = self.materialEditor

'''
start the application
'''
if __name__ == '__main__':
    ScreenmixApp().run()
