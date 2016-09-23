'''
Created on 02.06.2016

@author: mkennert

'''

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from materialEditor.iobserver import IObserver
from ownComponents.design import Design
from reinforcement.gui import ReinforcementEditorGui


class ReinforcementEditor(GridLayout, IObserver, ReinforcementEditorGui):
    
    '''
    the reinforcement-editor is the component, where you can edit the layers of a shape
    the shape-information is given by the cross-section-shape
    '''
    
    # cross-section-shape
    cs = ObjectProperty()
    
    # cross section
    crossSection = ObjectProperty()
    
    
    # constructor
    def __init__(self, **kwargs):
        super(ReinforcementEditor, self).__init__(**kwargs)
        self.cols, self.spacing = 1, Design.spacing
        self.containsInformation, self.error = False, False
  
    '''
    open the popup where the user can select the shape
    '''

    def show_shape_selection(self, btn):
        self.shapeSelection.open()
    
    '''
    look which shape the user has selected
    '''

    def finished_shape_selection(self, btn):
        if btn.text == self.rectangleStr:
            self.btnSelection.text = btn.text
            self.crossSection.show_rectangle_view()
        self.shapeSelection.dismiss()
    
    '''
    cancel the shape-selection
    '''
    def cancel_shape_selection(self):
        self.shapeSelection.dismiss()
        
    '''
    add the information of the selected shape
    '''
    def show_information(self, information):
        if not self.containsInformation:
            self.information = information
            self.add_widget(self.information, 3)
        else:
            self.remove_widget(self.information)
            self.information = information
            self.add_widget(self.information, 3)

    '''
    the method add_layer add a new layer at the cross section
    it use the choosen slidePercent value
    '''

    def add_layer(self, button):
        self.finished_adding()
        v = float(self.areaBtn.text)
        if v <= 0:
            return
        for i in range(0, len(self.allMaterials.allMaterials)):
            if self.allMaterials.allMaterials[i].name == self.btnMaterialOption.text:
                p = v / self.cs.size
                # proofs whether the layer is bigger as the cs
                if p > 1:
                    # wrong input
                    return
                self.cs.add_layer(p, self.allMaterials.allMaterials[i])
                return

    '''
    the method delete_layer was developed to delete a existing
    materials
    '''

    def delete_layer(self, button):
        self.cs.delete_layer()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.allMaterials = self.cs.allMaterials
        self.allMaterials.add_listener(self)
        self.create_gui()
