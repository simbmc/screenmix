'''
Created on 15.03.2016

@author: mkennert
'''
from abc import abstractmethod

from kivy.properties import StringProperty
class IView:
    
    '''
    IView is a interface which the views must implement. it makes sure,
    that the view has the necessary methods, which the other components
    are use
    '''
    ylabelStr = StringProperty('cross-section-height [m]')
    
    xlabelStr = StringProperty('cross-section-width [m]')
    
    #############################################################################
    # the following methods must implemented individual in the class,           #
    # which implements the interface                                            #
    #############################################################################
    
    @abstractmethod
    def add_layer(self, x, y, material):
        # should add a layer to the graph and 
        # safe the layer in a list
        raise NotImplemented('not implemented')

    @abstractmethod
    def delete_layer(self):
        # delete the layer from the graph
        raise NotImplemented('not implemented')

    @abstractmethod
    def create_graph(self):
        # create the graph where you can see the shape of
        # the cross-section
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def get_free_places(self):
        # return the places where's no layer. just the concrete
        # layers
        raise NotImplemented('not implemented')
    
    @abstractmethod
    def update_percent(self, value):
        # update the percent of the selected layer
        raise NotImplemented('not implemented')
    
    #############################################################################
    # the following methods must not implemented in the class,                  #
    # which implements the interface                                            #
    #############################################################################
    
    '''
    the method update_cs_information update the cross section information of 
    the view_information. this method must be called when the cross-section-size 
    or the layers of the cross-section has changed
    '''

    def update_cs_information(self):
        self.cs.calculate_strength()  # calculate the cracking stress
        self.cs.calculate_weight_price()
        self.cs.update_cs_information()
