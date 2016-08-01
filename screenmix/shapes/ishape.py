'''
Created on 26.07.2016

@author: mkennert
'''
from abc import abstractmethod


class IShape:

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_ack(self, ack):
        self.ack = ack

    '''
    the method add_layer add new materials in the view
    '''

    def add_layer(self, percent, material):
        self.view.add_layer(percent, material)

    '''
    the method delete_layer delete the selected materials
    '''

    def delete_layer(self):
        self.view.delete_layer()

    '''
    the method set_layer_information update the layer
    after a layer get the focus
    '''

    def set_layer_information(self, name, price, density, stiffness, strength, percent):
        self.refEdit.update_layer_information(name, price,
                                              density, stiffness,
                                              strength, percent)

    '''
    the method set_layer_information update the cross section information
    '''

    def set_cross_section_information(self):
        self.refEdit.update_cs_information(self.price,
                                           self.weight,
                                           self.strength)

    '''
    the method set_percent change the percentage share of the selected materials
    '''

    def set_percent(self, value):
        self.view.set_percent(value)

    ##########################################################################
    # the following methods must implemented individual in the class,           #
    # which implements the interface                                            #
    ##########################################################################
    
    @abstractmethod
    def calculate_weight_price(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def calculate_strength(self):
        raise NotImplemented('not implemented')

    @abstractmethod
    def set_reinforcement_editor(self, editor):
        raise NotImplemented('not implemented')
    
