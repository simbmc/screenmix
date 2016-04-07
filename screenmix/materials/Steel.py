'''
Created on 04.04.2016

@author: mkennert
'''
from materials import AMaterial

class Steel(AMaterial):
    def __init__(self):
        super.__init__(self,'Steel', 0.35,7850,210,350)
    
    