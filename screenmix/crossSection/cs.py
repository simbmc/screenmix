'''
Created on 15.03.2016
@author: mkennert
'''


from kivy.uix.gridlayout import GridLayout
from crossSectionView.rectangleView import CS_Rectangle_View 
from crossSectionView.csInformation import Cross_Section_Information
from materialEditor.materiallist import MaterialList

'''
the cross_Section was developed to undock the cs_information from the view
'''
class CrossSection(GridLayout): 
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSection, self).__init__(**kwargs)
        self.cross_section_height = 0.5
        self.cross_section_width = 0.25
        self.all_materials=MaterialList()
        self.view=CS_Rectangle_View()
        self.concrete_density=2300.
        self.concrete_price=0.065
        self.concrete_stiffness= 30000.
        self.concrete_strength= 3. 
        self.information=Cross_Section_Information()
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
        self.cross_section_height=value
    
    '''
    the method set_width change the width of the view
    ''' 
    def set_width(self,value):
        self.view.set_width(value)
        self.cross_section_width=value
        
    '''
    the method set_percent change the percentage share of the selected materials
    '''
    def set_percent(self, value):
        self.view.set_percent(value)
    
    '''
    calculate the weight and the price of the cross section
    '''
    def calculate_weight_price(self):
        weight=price=percent_of_layers=0.
        #go trough all layers and
        #get the weight of them
        for layer in self.view.layers:
            cur=layer.get_weight()
            weight+=cur
            price+=cur*layer.material.price
            percent_of_layers+=layer._height/self.cross_section_height
        #if the percent_of_layers is not 1 there is a matrix
        #with concrete as material
        weight+=(1-percent_of_layers)*self.cross_section_width*self.concrete_density
        price+=(1-percent_of_layers)*self.cross_section_height*self.cross_section_width*self.concrete_price
        self.weight=weight
        self.price=price
    
    '''
    the method calculate_strength calculate the strength of 
    the cross_section
    '''
    def calculate_strength(self):
        strength=0.
        #cur supremum
        self.min_of_maxstrain=10000000.
        #max strain is necessary for other calculations
        self.max_of_maxstrain=0
        percent_of_layers=0.
        #find the minimum max_strain and the maximum max_strain
        for layer in self.view.layers:
            percent_of_layers+=layer._height/self.cross_section_height
            cur_strain=layer.get_strain()
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
            strength+=self.min_of_maxstrain*layer.material.stiffness*layer._height/self.cross_section_height
        if 1.-percent_of_layers>0:
            strength+=self.min_of_maxstrain*(1.-percent_of_layers)*self.concrete_stiffness
        self.strength=strength
    
    '''
    calculate the strain of concrete
    '''
    def calculate_strain_of_concrete(self):
        return self.concrete_strength/self.concrete_stiffness
