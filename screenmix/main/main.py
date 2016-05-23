'''
Created on 14.04.2016

@author: mkennert
'''
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from ack_model.ack import Ack
from cross_section.crossSection import CrossSection
from designClass.design import Design
from material_editor.editor import Material_Editor


Window.size = (900, 600)
#Window.clearcolor = (1, 1, 1, 1)

class MainWindow(GridLayout):
    # Constructor
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 1
        self.btnSize=Design.btnSize
        self.allCrossSections=CrossSection()
        self.cs = self.allCrossSections.getCSRectangle()
        #Cross Section is the default view
        self.content = self.allCrossSections
        self.createPopup()
        self.createMenuBar()
        self.createComponets()

    '''
    create all components of the Scrollview root
    '''
    def createComponets(self):
        self.createCrossSectionView()
        self.createAckView()
        self.createMaterialEditor()

    '''
    create the list_view. here you can add more menu-options for the app
    '''
    def createListView(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        # CrossSectionRectangle
        cross_section = Button(
            text='cross section', size_hint_y=None, height=self.btnSize)
        cross_section.bind(on_press=self.showCrossSectionView)
        layout.add_widget(cross_section)
        # ack-view
        ack_view = Button(text='ack', size_hint_y=None, height=self.btnSize)
        ack_view.bind(on_press=self.showAckView)
        layout.add_widget(ack_view)
        # material-editor
        me = Button(text='material editor', size_hint_y=None, height=self.btnSize)
        me.bind(on_press=self.showMaterialEditor)
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
    def createPopup(self):
        self.createListView()
        self.popup = Popup(title='Menu', content=self.root, size_hint=(None, None), size=(
            300, 400), pos_hint=({'x': 0, 'top': 1}), pos=(0, 0))

    '''
    create the menu bar where you can select the 
    menu button to show the menu
    '''
    def createMenuBar(self):
        bar = GridLayout(cols=3, row_force_default=True,
                         row_default_height=self.btnSize, size_hint_y=None, height=self.btnSize)
        menu_button = Button(
            text='menu', size_hint_y=None, height=self.btnSize, size_hint_x=None, width=100)
        menu_button.bind(on_press=self.popup.open)
        bar.add_widget(menu_button)
        self.add_widget(bar)

    '''
    create the cross section
    '''
    def createCrossSectionView(self):
        self.add_widget(self.allCrossSections)

    '''
    create the ask_view
    '''
    def createAckView(self):
        self.ack_view = Ack()
        self.cs.setAck(self.ack_view)
        # sign in by the cross section
        self.ack_view.setCrossSection(self.cs)

    '''
    create the material-editor
    '''
    def createMaterialEditor(self):
        self.material_editor = Material_Editor()
        # sign in by the cross section
        self.material_editor.setCrossSection(self.allCrossSections)

    #############################################################################
    #Attention:When you want write a new show-method than you must make sure    #
    #that actually component is remove from the widget and set                  #
    #the content to the showed component                                        #
    #############################################################################
    
    '''
    show the ack-view
    '''
    def showAckView(self, button):
        self.ack_view.update()
        self.remove_widget(self.content)
        self.add_widget(self.ack_view)
        self.content = self.ack_view
        self.ack_view.update()
        self.popup.dismiss()
    
    '''
    show the cross-section-view
    '''
    def showCrossSectionView(self, button):
        self.remove_widget(self.content)
        self.add_widget(self.allCrossSections)
        self.content = self.allCrossSections
        self.popup.dismiss()
    
    '''
    show the material-editor
    '''
    def showMaterialEditor(self, button):
        self.remove_widget(self.content)
        self.add_widget(self.material_editor)
        self.content = self.material_editor
        self.popup.dismiss()

class CSIApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    CSIApp().run()
