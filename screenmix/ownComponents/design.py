'''
Created on 29.04.2016

@author: mkennert
'''

from kivy.metrics import dp, sp


class Design:
    '''
    the class design contains just attributes for the design
    '''
    #size-properties
    btnHeight = dp(40)
    lblHeight=dp(10)
    font_size=sp(13)
    spacing=dp(5)
    c=10
    padding=[dp(c),dp(5),dp(c),dp(5)]
    #color properties
    focusColor =[0,0,0,1]
    btnColor=[0.1, 0.1, 0.1, 1]
    btnForeground=[1, 1, 1, 1]
    foregroundColor=[0,0,0,1]
