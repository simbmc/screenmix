'''
Created on 15.03.2016
@author: mkennert
'''


from kivy.uix.gridlayout import GridLayout
from crossSectionView.rectangleView import CSRectangleView 
from crossSectionView.csInformation import CrossSectionInformation
from materialEditor.materiallist import MaterialList

'''
the cross_Section was developed to undock the cs_information from the view
'''
class CrossSection(GridLayout): 
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.h = 0.5
        self.w = 0.25
        self.allMaterials=MaterialList()
        self.view=CSRectangleView()
        self.concreteDensity=2300.
        self.concretePrice=0.065
        self.concreteStiffness= 30000.
        self.concreteStrength= 3. 
        self.information=CrossSectionInformation()
        self.cols=2
        self.add_widget(self.view)
        self.add_widget(self.information)
        self.view.set_cross_section(self)
        self.information.set_cross_section(self)
        self.calculate_weight_price()
        self.calculate_strength()
        self.set_cross_section_information()
    
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''
    def set_ack(self,ack):
        self.ack=ack
    
    '''
    the method add_layer add new materials in the view
    '''
    def add_layer(self,percent,material):
        self.view.add_layer(percent,material)
        
    '''
    the method delete_layer delete the selected materials
    '''
    def delete_layer(self):
        self.view.delete_layer()
        
    '''
    the method set_layer_information update the layer
    after a layer get the focus
    '''
    def set_layer_information(self,name,price,density,stiffness,strength,percent):
        self.information.update_layer_information(name,price,density,stiffness,strength,percent)
    
    '''
    the method set_layer_information update the cross section information
    '''
    def set_cross_section_information(self):
        self.information.update_cross_section_information(self.price, self.weight, self.strength)
    
    '''
    get all the layers
    '''
    def get_layers(self):
        return self.view.get_layers()
    
    '''
    the method set_height changes the height of the view
    '''
    def set_height(self,value):
        self.view.set_height(value)
        self.h=value
    
    '''
    the method set_width change the width of the view
    ''' 
    def set_width(self,value):
        self.view.set_width(value)
        self.w=value
        
    '''
    the method set_percent change the percentage share of the selected materials
    '''
    def set_percent(self, value):
        self.view.set_percent(value)
    
    '''
    calculate the weight and the price of the cross section
    '''
    def calculate_weight_price(self):
        weight=price=percentOfLayers=0.
        #go trough all layers and
        #get the weight of them
        for layer in self.view.layers:
            cur=layer.get_weight()
            weight+=cur
            price+=cur*layer.material.price
            percentOfLayers+=layer.h/self.h
        #if the percentOfLayers is not 1 there is a matrix
        #with concrete as material
        weight+=(1-percentOfLayers)*self.w*self.concreteDensity
        price+=(1-percentOfLayers)*self.h*self.w*self.concretePrice
        self.weight=weight
        self.price=price
    
    '''
    the method calculate_strength calculate the strength of 
    the cross_section
    '''
    def calculate_strength(self):
        strength=0.
        #cur supremum
        self.minOfMaxstrain=1e6
        #max strain is necessary for other calculations
        self.maxOfMaxstrain=0
        percentOfLayers=0.
        #find the minimum max_strain and the maximum max_strain
        for layer in self.view.layers:
            percentOfLayers+=layer.h/self.h
            curStrain=layer.get_strain()
            #proof whether the curStrain is smaller as the min
            if curStrain<self.minOfMaxstrain:
                self.minOfMaxstrain=curStrain
            #proof whether the curStrain is bigger as the max
            if curStrain>self.maxOfMaxstrain:
                self.maxOfMaxstrain=curStrain
        #if the percentOfLayers is not 1 there is a matrix
        #with concrete as material
        if 1.-percentOfLayers>0:
            curValue=self.concreteStrength/self.concreteStiffness
            if self.minOfMaxstrain>curValue:
                self.minOfMaxstrain=curValue
            if self.maxOfMaxstrain<curValue:
                self.maxOfMaxstrain=curValue
        #calculate the strength
        for layer in self.view.layers:
            strength+=self.minOfMaxstrain*layer.material.stiffness*layer.h/self.h
        if 1.-percentOfLayers>0:
            strength+=self.minOfMaxstrain*(1.-percentOfLayers)*self.concreteStiffness
        self.strength=strength
    
    '''
    calculate the strain of concrete
    '''
    def calculate_strain_of_concrete(self):
        return self.concreteStrength/self.concreteStiffness
