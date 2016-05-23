'''
Created on 15.03.2016

@author: mkennert
'''


from kivy.uix.gridlayout import GridLayout
from cross_section_view.cs_rectangle_view import CS_Rectangle_View
from cross_section_information.cs_information import Cross_Section_Information
from material_editor.materiallist import MaterialList
from cross_section.ashape import AShape

'''
the cross_Section was developed to undock the cs_information from the view
'''
class CrossSectionRectangle(GridLayout,AShape): 
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSectionRectangle, self).__init__(**kwargs)
        self.cheight = 0.5
        self.cw = 0.25
        self.concrete_density=2300.
        self.concrete_price=0.065
        self.concrete_stiffness= 30000.
        self.concrete_strength= 3.
        self.view=CS_Rectangle_View() 
        self.view.setCrossSection(self)
        #self.information=Cross_Section_Information()
        #self.information.setCrossSection(self)
        
    def setInformation(self,information):
        self.information=information
        self.calculateWeightPrice()
        self.calculateStrength()
        self.setCrossSectionInformation()
    
    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''
    def setAck(self,ack):
        self.ack=ack
    
    '''
    the method addLayer add new materials in the view
    '''
    def addLayer(self,percent,material):
        self.view.addLayer(percent,material)
        
    '''
    the method deleteLayer delete the selected materials
    '''
    def deleteLayer(self):
        self.view.deleteLayer()
        
    '''
    the method setLayerInformation update the layer
    after a layer get the focus
    '''
    def setLayerInformation(self,name,price,density,stiffness,strength,percent):
        self.information.updateLayerInformation(name,price,density,stiffness,strength,percent)
    
    '''
    the method setLayerInformation update the cross section information
    '''
    def setCrossSectionInformation(self):
        self.information.updateCrossSectionInformation(self.price, self.weight, self.strength)
    
    '''
    get all the layers
    '''
    def getLayers(self):
        return self.view.getLayers()
    
    '''
    the method setHeight changes the height of the view
    '''
    def setHeight(self,value):
        self.view.setHeight(value)
        self.cheight=value
    
    '''
    the method setWidth change the width of the view
    ''' 
    def setWidth(self,value):
        self.view.setWidth(value)
        self.cw=value
        
    '''
    the method setPercent change the percentage share of the selected materials
    '''
    def setPercent(self, value):
        self.view.setPercent(value)
    
    '''
    calculate the weight and the price of the cross section
    '''
    def calculateWeightPrice(self):
        weight=price=percent_of_layers=0.
        #go trough all layers and
        #get the weight of them
        for l in self.view.layers:
            cur=l.getWeight()
            weight+=cur
            price+=cur*l.material.price
            percent_of_layers+=l.h/self.cheight
        #if the percent_of_layers is not 1 there is a matrix
        #with concrete as material
        weight+=(1-percent_of_layers)*self.cw*self.concrete_density
        price+=(1-percent_of_layers)*self.cheight*self.cw*self.concrete_price
        self.weight=weight
        self.price=price
    
    '''
    the method calculateStrength calculate the strength of 
    the cross_section
    '''
    def calculateStrength(self):
        strength=0.
        #cur supremum
        self.min_of_maxstrain=10000000.
        #max strain is necessary for other calculations
        self.max_of_maxstrain=0
        percent_of_layers=0.
        #find the minimum max_strain and the maximum max_strain
        for layer in self.view.layers:
            percent_of_layers+=layer.h/self.cheight
            cur_strain=layer.getStrain()
            #proof whether the cur_strain is smaller as the min
            if cur_strain<self.min_of_maxstrain:
                self.min_of_maxstrain=cur_strain
            #proof whether the cur_strain is bigger as the max
            if cur_strain>self.max_of_maxstrain:
                self.max_of_maxstrain=cur_strain
        #if the percent_of_layers is not 1 there is a matrix
        #with concrete as material
        if 1.-percent_of_layers>0:
            cur_value=self.concrete_strength/self.concrete_stiffness
            if self.min_of_maxstrain>cur_value:
                self.min_of_maxstrain=cur_value
            if self.max_of_maxstrain<cur_value:
                self.max_of_maxstrain=cur_value
        #calculate the strength
        for layer in self.view.layers:
            strength+=self.min_of_maxstrain*layer.material.stiffness*layer.h/self.cheight
        if 1.-percent_of_layers>0:
            strength+=self.min_of_maxstrain*(1.-percent_of_layers)*self.concrete_stiffness
        self.strength=strength
    
    '''
    calculate the strain of concrete
    '''
    #def calculate_strain_of_concrete(self):
    #    return self.concrete_strength/self.concrete_stiffness
    
    def signParent(self, allcrossection):
        self.allCrossSection=allcrossection
        self.information=allcrossection.getInformation()
        