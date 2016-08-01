'''
Created on 26.07.2016

@author: mkennert
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar, ActionPrevious
from kivy.uix.gridlayout import GridLayout

from ackModel.ack import Ack
from crossSection.crossSection import CrossSection
from materialEditor.editor import Material_Editor


Window.size = (720, 500)
Window.clearcolor = (1, 1, 1, 0.5)

'''
create the Actionbar in the mainMenu with the kv.file screenmixapp
'''
class AppActionBar(ActionBar):
    pass

'''
create the ActionMenu in the mainMenu with the kv.file screenmixapp
'''
class ActionMenu(ActionPrevious):
    pass

'''
starts the application
'''
Window.clearcolor = (1, 1, 1, 0.5)
class ScreenmixApp(App):
    def build(self):
        self.content = GridLayout(cols=1, spacing=5)
        bar = AppActionBar()
        self.content.add_widget(bar)
        self.content.cols = 1
        self.create_componets()
        # Cross Section is the default view
        self.contentLayout = self.cs
        return self.content
    
    '''
    create all components of the Scrollview root
    '''

    def create_componets(self):
        self.create_cross_section_view()
        self.create_ack_view()
        self.create_material_editor()


    '''
    create the cross section
    '''

    def create_cross_section_view(self):
        self.cs = CrossSection()
        self.content.add_widget(self.cs)

    '''
    create the ask_view
    '''

    def create_ack_view(self):
        self.ackView = Ack()
        self.cs.shapeRectangle.set_ack(self.ackView.ackRect)
        self.ackView.ackRect.set_cross_section(self.cs.shapeRectangle)
        # when you add more shapes, make sure that the
        # shapes has a ownAck

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = Material_Editor()
        self.materialEditor.set_cross_section(self.cs.shapeRectangle)

    ##########################################################################
    # Attention:When you want write a new show-method than you must make sure    #
    # that actually component is remove from the widget and set                  #
    # the contentLayout to the showed component                                  #
    ##########################################################################

    '''
    show the ack-view
    '''

    def show_ack_view(self):
        self.ackView.content.update()
        self.content.remove_widget(self.contentLayout)
        self.content.add_widget(self.ackView)
        self.contentLayout = self.ackView

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
        self.content.remove_widget(self.contentLayout)
        self.content.add_widget(self.materialEditor)
        self.contentLayout = self.materialEditor
    
if __name__ == '__main__':
    ScreenmixApp().run()