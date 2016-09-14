'''
Created on 25.07.2016

@author: mkennert
'''
from decimal import Decimal

from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from crossSectionInformation.rectInformation import RectangleInformation
from crossSectionView.rectView import RectView
from materialEditor.materiallist import MaterialList
from materials.concrete import Concrete
from shapes.ishape import IShape


class ShapeRectangle(GridLayout, IShape):
    
    '''
    represents a cross section which has the shape 
    of a rectangle
    '''
    
    # important components
    view = ObjectProperty()
    
    # information- rectangle
    information = ObjectProperty()
    
    # ack-rectangle
    ack = ObjectProperty()
    
    # layer of the cross-section-shape
    layers = ListProperty([])
    
    # height of the rectangle
    h = NumericProperty(0.5)
    
    # width of the rectangle
    w = NumericProperty(0.25)
    
    # area of the rectangle
    size = NumericProperty(0.25 * 0.5)
    
    # weight of the rectangle
    weight = NumericProperty()
    
    # price of the rectangle
    price = NumericProperty()
    
    # cracking-stress of the rectangle
    strength = NumericProperty()

    # constructor
    def __init__(self, **kwargs):
        super(ShapeRectangle, self).__init__(**kwargs)
        self.cols = 2
        self.allMaterials = MaterialList.Instance()
        concrete = Concrete()
        self.concreteDensity, self.concretePrice = concrete.density, concrete.price
        self.concreteStiffness, self.concreteStrength = concrete.stiffness, concrete.strength
        self.concreteStrain = self.concreteStrength / self.concreteStiffness
        self.information, self.view = RectangleInformation(), RectView()
    
    '''
    update the concrete-properties
    '''
    def update_concrete_information(self, density, price, stiffness, strength):
        self.concreteDensity, self.concretePrice = density, price
        self.concreteStiffness, self.concreteStrength = stiffness, strength
        self.concreteStrain = self.concreteStrength / self.concreteStiffness
        
    '''
    the method update_height changes the height of the view
    '''

    def update_height(self, value):
        self.view.update_height(value)
        self.h = value
        self.size = self.h * self.w
        for layer in self.layers:
            if layer.focus:
                self.refEdit.areaInput.text = '%.2E' % Decimal(str(self.size * layer.p))
        
    '''
    the method update_width change the width of the view
    '''

    def update_width(self, value):
        self.view.update_width(value)
        self.w = value
        self.size = self.h * self.w
        for layer in self.layers:
            if layer.focus:
                self.refEdit.areaInput.text = '%.2E' % Decimal(str(self.size * layer.p))
        
    '''
    calculate the weight and the lblPrice of the cross section
    '''

    def calculate_weight_price(self):
        weight = price = 0.
        freeplaces = self.view.get_free_places()
        # go trough all layers and
        # get the weight of them
        for layer in self.layers:
            cur = layer.get_weight()
            weight += cur
            price += cur * layer.material.price
        # get the free places, where the material is concrete
        for layer in freeplaces:
            w = (layer[1] - layer[0]) * self.w * self.concreteDensity
            weight += w
            price += w * self.concretePrice
        self.weight, self.price = weight, price

    '''
    the method calculate_strength calculate the strength of 
    the cross_section
    '''

    def calculate_strength(self):
        strength = 0.
        # cur supremum
        self.minOfMaxstrain = 1e6
        # max strain is necessary for other calculations
        self.maxOfMaxstrain = 0
        # find the minimum max_strain and the maximum max_strain
        for layer in self.layers:
            curStrain = layer.strain
            # proof whether the curStrain is smaller as the min
            if curStrain < self.minOfMaxstrain:
                self.minOfMaxstrain = curStrain
            # proof whether the curStrain is bigger as the max
            if curStrain > self.maxOfMaxstrain:
                self.maxOfMaxstrain = curStrain
        # if the percentOfLayers is not 1 there is a matrix
        # with concrete as material
        freePlaces = self.view.get_free_places()
        if len(freePlaces) > 0:
            curValue = self.concreteStrength / self.concreteStiffness
            if self.minOfMaxstrain > curValue:
                self.minOfMaxstrain = curValue
            if self.maxOfMaxstrain < curValue:
                self.maxOfMaxstrain = curValue
        # calculate the strength
        for layer in self.layers:
            strength += self.minOfMaxstrain * \
                layer.material.stiffness * layer.h / self.h
        for layer in freePlaces:
            strength += self.minOfMaxstrain * \
                (layer[1] - layer[0]) / self.h * self.concreteStiffness
        self.strength = strength


    '''
    set the editor
    '''

    def set_reinforcement_editor(self, editor):
        self.refEdit = editor
        self.information.cs = self
        self.information.create_gui()
        self.view.cs = self
        self.calculate_weight_price()
        self.calculate_strength()
        self.update_cs_information()
