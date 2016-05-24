'''
Created on 12.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionInformation.csInformation import CrossSectionInformation
from materialEditor.materiallist import MaterialList
from shapes.shapeDoubleT import CrossSectionDoubleT
from shapes.shapeRectangle import CrossSectionRectangle


class CrossSection(GridLayout):
    #Constructor
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols=2
        self.allMaterials=MaterialList()
        self.csRectangle=CrossSectionRectangle()
        self.csDoubleT=CrossSectionDoubleT()
        self.view=self.csRectangle.view
        self.information=CrossSectionInformation()
        self.information.setCrossSection(self)
        self.add_widget(self.csRectangle.view)
        self.add_widget(self.information)
        self.csRectangle.setInformation(self.information)
        self.csDoubleT.setInformation(self.information)
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
    def showRectangleView(self):
        self.remove_widget(self.view)
        self.view=self.csRectangle.view
        self.add_widget(self.view, 1)
    
    '''
    show doubleT-view
    '''
    def showDoubleTView(self):
        self.remove_widget(self.view)
        self.view=self.csDoubleT.view
        self.add_widget(self.view, 1)
    
    '''
    get the information-component
    '''
    def getInformation(self):
        return self.information