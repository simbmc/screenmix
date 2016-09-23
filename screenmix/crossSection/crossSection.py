'''
Created on 25.07.2016

@author: mkennert
'''
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from materialEditor.materiallist import MaterialList
from reinforcement.editor import ReinforcementEditor
from shapes.shapeRectangle import ShapeRectangle


class CrossSection(GridLayout):
    
    '''
    cross section contains all shapes. it manage which shape should be show
    '''
    
    # ack-component
    ack = ObjectProperty()
    
    # reinforcement-editor
    reEdit = ObjectProperty(ReinforcementEditor())
    
    # materiallist
    allMaterials = ObjectProperty(MaterialList.Instance())
    
    # view of the cross section
    view = ObjectProperty()
    
    # shapes
    shapeRectangle = ObjectProperty(ShapeRectangle())
    ###################################
    # here you can add more shapes    #
    ###################################
    
    # constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols = 2
        self.padding = [5, 0, 5, 0]
        self.spacing = dp(10) 
        # default shape is rectangle        
        self.view = self.shapeRectangle.view
        self.reEdit.set_cross_section(self.shapeRectangle)
        self.reEdit.crossSection = self
        self.shapeRectangle.set_reinforcement_editor(self.reEdit)
        self.reEdit.show_information(self.shapeRectangle.information)
        self.add_widget(self.view)
        self.add_widget(self.reEdit)
    
    ######################################################
    # When you add more shapes, make sure that the shapes#
    # has a show-method like show_rectangle_view         #
    ######################################################
    
    '''
    show the rectangle view
    '''

    def show_rectangle_view(self):
        if self.view==self.shapeRectangle.view:
            return
        # delete the current view and add the new shape
        self.remove_widget(self.view)
        self.view = self.shapeRectangle.view
        self.add_widget(self.view)
        # show the shape in the reinforcementEditor and in the ack-menu
        self.reEdit.show_information(self.shapeRectangle.information)
        self.ack.show_ack_rect()
    
    '''
    update the informations of the shapes when the user
    edit the material
    '''
        
    def update_informations(self):
        self.shapeRectangle.view.update_cs_information()
        # when you add new shapes, make sure that the shape has a update 
        # method
    
    '''
    update the concrete-properties
    '''
        
    def update_concrete_information(self, density, price, stiffness, strength):
        # when you add more shapes, make sure that your shape makes a update when the 
        # concrete has changed
        self.shapeRectangle.update_concrete_information(density, price, stiffness, strength)
