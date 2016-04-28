'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from ack_model.ack import Ack
from cross_section.cs import Cross_Section
from material_editor.editor import Material_Editor
from kivy.core.window import Window
Window.size = (720, 500)


class MainWindow(GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 1
        self.create_popup()
        self.create_menu_bar()
        self.create_componets()
        # Cross Section is the default view
        self.content = self.cross_section

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
        # Cross_Section
        cross_section = Button(
            text='cross section', size_hint_y=None, height=40)
        cross_section.bind(on_press=self.show_cross_section_view)
        layout.add_widget(cross_section)
        # ack-view
        ack_view = Button(text='ack', size_hint_y=None, height=40)
        ack_view.bind(on_press=self.show_ack_view)
        layout.add_widget(ack_view)
        # material-editor
        me = Button(text='material editor', size_hint_y=None, height=40)
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
            250, self.height * 2), pos_hint=({'x': 0, 'top': 1}), pos=(0, 0))

    '''
    create the menu bar where you can select the 
    menu button to show the menu
    '''

    def create_menu_bar(self):
        bar_height = 25
        bar = GridLayout(cols=3, row_force_default=True,
                         row_default_height=bar_height, size_hint_y=None, height=25)
        menu_button = Button(
            text='menu', size_hint_y=None, height=bar_height, size_hint_x=None, width=100)
        menu_button.bind(on_press=self.popup.open)
        bar.add_widget(menu_button)
        self.add_widget(bar)

    '''
    create the cross section
    '''

    def create_cross_section_view(self):
        self.cross_section = Cross_Section()
        self.add_widget(self.cross_section)

    '''
    create the ask_view
    '''

    def create_ack_view(self):
        self.ack_view = Ack()
        self.cross_section.set_ack(self.ack_view)
        # sign in by the cross section
        self.ack_view.set_cross_section(self.cross_section)

    '''
    create the material-editor
    '''

    def create_material_editor(self):
        self.material_editor = Material_Editor()
        # sign in by the cross section
        self.material_editor.set_cross_section(self.cross_section)

    ##########################################################################
    #Attention:When you want write a new show-method than you must make sure    #
    #that actually component is remove from the widget and set                  #
    #the content to the showed component                                        #
    ##########################################################################
    def show_ack_view(self, button):
        self.ack_view.update()
        self.remove_widget(self.content)
        self.add_widget(self.ack_view)
        self.content = self.ack_view
        self.popup.dismiss()

    def show_cross_section_view(self, button):
        self.remove_widget(self.content)
        self.add_widget(self.cross_section)
        self.content = self.cross_section
        self.popup.dismiss()

    def show_material_editor(self, button):
        self.remove_widget(self.content)
        self.add_widget(self.material_editor)
        self.content = self.material_editor
        self.popup.dismiss()

class CSIApp(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    CSIApp().run()
