'''
Created on 04.04.2016

@author: mkennert
'''
from materials.amaterial import AMaterial

class Carbon_Fiber(AMaterial):
    def __init__(self):
        super(Carbon_Fiber,self,).__init__('carbon fiber', 20,1600.,250000.,1600.)

