'''
Created on 04.04.2016

@author: mkennert
'''
from materials import AMaterial

class Concrete(AMaterial):
    def __init__(self):
        super.__init__(self,'Concrete', 0.065,2300,30,30)
        