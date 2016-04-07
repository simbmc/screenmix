'''
Created on 04.04.2016

@author: mkennert
'''
from materials import AMaterial

class Glass_Fiber(AMaterial):
    def __init__(self):
        super.__init__(self,'Glass fiber', 2,2660,50,1000)