'''
Created on 14.04.2016
@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from ackModel.ack import Ack
from crossSection.cs import CrossSection
from materialEditor.editor import Material_Editor
from kivy.core.window import Window
from designClass.design import Design
Window.size = (720, 500)


class Main(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.cols = 1
        self.btnSize = Design.btnSize
        self.create_popup()
        self.create_menu_bar()
        self.create_componets()
        # Cross Section is the default view
        self.content = self.cs

    '''
    create all components of the Scrollview root
    '''

    def create_componets(self):
        self.create_cross_section_view()
        self.create_ack_view()
        self.create_material_editor()

    '''
    create the list_view. here you can add more menu-options for the app
    '''

    def create_list_view(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        # CrossSection
        crossSection = Button(
            text='cross section', size_hint_y=None, height=self.btnSize)
        crossSection.bind(on_press=self.show_cross_section_view)
        layout.add_widget(crossSection)
        # ack-view
        ackView = Button(text='ack', size_hint_y=None, height=self.btnSize)
        ackView.bind(on_press=self.show_ack_view)
        layout.add_widget(ackView)
        # material-editor
        me = Button(
            text='material editor', size_hint_y=None, height=self.btnSize)
        me.bind(on_press=self.show_material_editor)
        layout.add_widget(me)
        ##################################################################
        #Here you can add more menu-parts                                #
        #Attention: it's necessary that the button have the follow       #
        #properties: size_hint_y=None, height=40                         #
        ##################################################################
        self.root = ScrollView()
        self.root.add_widget(layout)

    '''
    create the popup with the menu options
    '''

    def create_popup(self):
        self.create_list_view()
        self.popup = Popup(title='Menu', content=self.root, size_hint=(None, None), size=(
            300, 400), pos_hint=({'x': 0, 'top': 1}), pos=(0, 0))

    '''
    create the menu bar where you can select the 
    menu button to show the menu
    '''

    def create_menu_bar(self):
        bar = GridLayout(cols=3, row_force_default=True,
                         row_default_height=self.btnSize, size_hint_y=None, height=self.btnSize)
        menuButton = Button(
            text='menu', size_hint_y=None, height=self.btnSize, size_hint_x=None, width=100)
        menuButton.bind(on_press=self.popup.open)
        bar.add_widget(menuButton)
        self.add_widget(bar)

    '''
    create the cross section
    '''

    def create_cross_section_view(self):
        self.cs = CrossSection()
        self.add_widget(self.cs)

    '''
    create the ask_view
    '''

    def create_ack_view(self):
        self.ackView = Ack()
        self.cs.set_ack(self.ackView)
        # sign in by the cross section
        self.ackView.set_cross_section(self.cs)

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.materialEditor = Material_Editor()
        # sign in by the cross section
        self.materialEditor.set_cross_section(self.cs)

    ##########################################################################
    #Attention:When you want write a new show-method than you must make sure    #
    #that actually component is remove from the widget and set                  #
    #the content to the showed component                                        #
    ##########################################################################

    '''
    show the ack-view
    '''

    def show_ack_view(self, button):
        self.ackView.update()
        self.remove_widget(self.content)
        self.add_widget(self.ackView)
        self.content = self.ackView
        self.ackView.update()
        self.popup.dismiss()

    '''
    show the cross section view
    '''

    def show_cross_section_view(self, button):
        self.remove_widget(self.content)
        self.add_widget(self.cs)
        self.content = self.cs
        self.popup.dismiss()

    '''
    show the material-editor
    '''

    def show_material_editor(self, button):
        self.remove_widget(self.content)
        self.add_widget(self.materialEditor)
        self.content = self.materialEditor
        self.popup.dismiss()


class CSIApp(App):

    def build(self):
        return Main()

if __name__ == '__main__':
    CSIApp().run()
