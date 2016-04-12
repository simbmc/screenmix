'''
Created on 04.04.2016

@author: mkennert
'''
from materials.AMaterial import AMaterial

class Glass_Fiber(AMaterial):
    def __init__(self):
        super(Glass_Fiber,self,).__init__('glass fiber', 2,2660.,50000.,1000.)

