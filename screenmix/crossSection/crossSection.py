'''
Created on 25.07.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from materialEditor.materiallist import MaterialList
from reinforcement.editor import ReinforcementEditor
from shapes.shapeRectangle import ShapeRectangle


class CrossSection(GridLayout):
    # Constructor
    
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols = 2
        self.padding = [10, 10, 10, 10]
        self.allMaterials = MaterialList.get_instance()
        # shapes
        self.shapeRectangle = ShapeRectangle()
        ###################################
        # here you can add more shapes    #
        ###################################
        self.reinforcmentEditor = ReinforcementEditor()
        # default shape is rectangle        
        self.view = self.shapeRectangle.view
        self.reinforcmentEditor.set_cross_section(self.shapeRectangle)
        self.shapeRectangle.set_reinforcement_editor(self.reinforcmentEditor)
        self.reinforcmentEditor.show_information(self.shapeRectangle.information)
        self.add_widget(self.view)
        self.add_widget(self.reinforcmentEditor)

    '''
    show the rectangle view
    '''

    def show_rectangle_view(self):
        # delete the current view and add the new shape
        self.remove_widget(self.view)
        self.view = self.csRectangle.view
        self.add_widget(self.view)
        # show the shape in the reinforcementEditor and in the ack-menu
        self.reinforcmentEditor.show_information(self.shapeRectangle.information)
        self.ack.show_ack_rect()
    
    ######################################################
    # When you add more shapes, make sure that the shapes#
    # has a show-method like show_rectangle_view         #
    ######################################################
    
    '''
    set the ack
    '''
    def set_ack(self, ack):
        self.ack = ack
    
