'''
Created on 29.04.2016

@author: mkennert
'''

from kivy.metrics import dp, sp


class Design:
    
    '''
    the class design contains just attributes for the design
    '''
    
    # size-properties
    btnHeight = dp(40)
    lblHeight = dp(10)
    font_size = sp(13)  # font-size for lbls
    spacing = dp(5)  # spacing between components
    padding = [dp(10), dp(0), dp(10), dp(10)]
    deltaCircle = 50.
    # color properties
    focusColor = [0, 0, 0, 1]  # focus-color of the graphs
    btnColor = [0.1, 0.1, 0.1, 1]  # background
    btnForeground = [1, 1, 1, 1]  # foreground
    popupForeground = [0, 0, 0, 1]  # popup-foreground
