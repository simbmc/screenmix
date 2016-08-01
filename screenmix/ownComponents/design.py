'''
Created on 29.04.2016

@author: mkennert
'''

'''
the class design contains just attributes for the design
'''

from itertools import cycle

from kivy.metrics import dp


class Design:
    btnHeight = dp(40)
    lblHeight=dp(10)
    focusColor =[0,0,0,1]
    btnColor=[0.1, 0.1, 0.1, 1]
    btnForeground=[1, 1, 1, 1]
    foregroundColor=[0,0,0,1]
