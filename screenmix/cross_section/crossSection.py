'''
Created on 12.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from cross_section.cross_section_doubleT import CrossSectionDoubleT
from cross_section.cross_section_rectangle import CrossSectionRectangle
from cross_section_information.cs_information import Cross_Section_Information
from material_editor.materiallist import MaterialList


class CrossSection(GridLayout):
    #Constructor
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cols=2
        self.all_materials=MaterialList()
        self.csRectangle=CrossSectionRectangle()
        self.csDoubleT=CrossSectionDoubleT()
        self.view=self.csRectangle.view
        self.information=Cross_Section_Information()
        self.information.setCrossSection(self)
        self.add_widget(self.csRectangle.view)
        self.add_widget(self.information)
        self.csRectangle.setInformation(self.information)
        self.csDoubleT.setInformation(self.information)
        #circle not finished yet
    
    '''
    return the CS-Rectangle
    '''
    def getCSRectangle(self):
        return self.csRectangle
    
    '''
    '''
    def getCSDoubleT(self):
        return self.csDoubleT
    
    '''
    '''
    def showRectangleView(self):
        self.remove_widget(self.view)
        self.view=self.csRectangle.view
        self.add_widget(self.view, 1)
    
    '''
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