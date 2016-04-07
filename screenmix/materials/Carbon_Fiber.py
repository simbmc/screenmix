'''
Created on 04.04.2016

@author: mkennert
'''
from materials import AMaterial

class Carbon_Fiber(AMaterial):
    def __init__(self):
        super.__init__(self,'Carbon fiber', 20,1600,250,1600)