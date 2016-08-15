'''
Created on 11.05.2016

@author: mkennert
'''
from abc import abstractmethod


class IObserver:
    
    '''
    iobserver must implement by the components, which contains
    the materiallist. so when the materiallist has changed the 
    oberserver must update the view
    '''
    
    '''
    update the listen when the materiallist
    has changed
    '''
    @abstractmethod
    def update(self):
        raise NotImplemented('not implemented')