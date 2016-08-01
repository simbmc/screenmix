'''
Created on 25.07.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout
from crossSectionView.rectView import RectView
from materialEditor.materiallist import MaterialList
from materials.concrete import Concrete
from crossSectionInformation.rectInformation import RectangleInformation
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from shapes.ishape import IShape


class ShapeRectangle(GridLayout, IShape):
    h, w = NumericProperty(), NumericProperty()
    weight, price = NumericProperty(), NumericProperty()
    strength = NumericProperty()
    view, information = ObjectProperty(), ObjectProperty()
    ack = ObjectProperty()
    layers = ListProperty([])

    # Constructor
    def __init__(self, **kwargs):
        super(ShapeRectangle, self).__init__(**kwargs)
        self.h, self.w = 0.5, 0.25
        self.cols = 2
        self.allMaterials, concrete = MaterialList.get_instance(), Concrete()
        self.concreteDensity, self.concretePrice = concrete.density, concrete.price
        self.concreteStiffness, self.concreteStrength = concrete.stiffness, concrete.strength
        self.information, self.view = RectangleInformation(), RectView()

    '''
    the method set_height changes the height of the view
    '''

    def set_height(self, value):
        self.view.set_height(value)
        self.h = value

    '''
    the method set_width change the width of the view
    '''

    def set_width(self, value):
        self.view.set_width(value)
        self.w = value


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
            curStrain = layer.get_strain()
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
    calculate the strain of concrete
    '''

    def calculate_strain_of_concrete(self):
        return self.concreteStrength / self.concreteStiffness

    '''
    set the editor
    '''

    def set_reinforcement_editor(self, editor):
        self.refEdit = editor
        self.information.set_cross_section(self)
        self.view.set_cross_section(self)
        self.calculate_weight_price()
        self.calculate_strength()
        self.set_cross_section_information()
    
    