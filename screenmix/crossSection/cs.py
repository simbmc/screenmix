'''
Created on 12.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionInformation.csInformation import CrossSectionInformation
from materialEditor.materiallist import MaterialList
from shapes.shapeDoubleT import ShapeDoubleT
from shapes.shapeRectangle import shapeRectangle


class CrossSection(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols=2
        self.allMaterials=MaterialList()
        self.csRectangle=shapeRectangle()
        self.csDoubleT=ShapeDoubleT()
        self.view=self.csRectangle.view
        #self.csRectangle.setInformation(self.information)
        #self.csDoubleT.setInformation(self.information)
        #circle not finished yet
    
    
    '''
    return the cs-rectangle
    '''
    def getCSRectangle(self):
        return self.csRectangle
    
    '''
    return the cs-doubleT
    '''
    def getCSDoubleT(self):
        return self.csDoubleT
    
    '''
    show rectangle-view
    '''
    def setRectangleView(self):
        self.remove_widget(self.view)
        self.view=self.csRectangle.view
        self.reEditor.changeCrossSection(self.view)
    
    '''
    show doubleT-view
    '''
    def setDoubleTView(self):
        self.remove_widget(self.view)
        self.view=self.csDoubleT.view
        self.reEditor.changeCrossSection(self.view)
    
    '''
    get the information-component
    '''
    def getInformation(self):
        return self.information
    
    '''
    set the cross section editor
    '''
    def setCrossSectionEditor(self, csEditor):
        self.csEditor=csEditor
    
    '''
    set the reinforcement editor
    '''
    def setReinforcementEditor(self,reEditor):
        self.reEditor=reEditor
        self.csRectangle.setInformation(reEditor)
        self.csDoubleT.setInformation(reEditor)