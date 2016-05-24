'''
Created on 13.05.2016

@author: mkennert
'''
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from materialEditor.numpad import Numpad


class DoubleTInformation(GridLayout):
    #Constructor
    def __init__(self, **kwargs):
        super(DoubleTInformation, self).__init__(**kwargs)
        self.focusBtn=None
        self.cols=2
    '''
    create the gui
    '''
    def createGui(self):
        self.topWidth=Button(text=str(self.cs.getWidthTop()))
        self.middleWidth=Button(text=str(self.cs.getWidthMiddle()))
        self.bottomWidth=Button(text=str(self.cs.getWidthBottom()))
        self.topHeight=Button(text=str(self.cs.getHeightTop()))
        self.middleHeight=Button(text=str(self.cs.getHeightMiddle()))
        self.bottomHeight=Button(text=str(self.cs.getHeightBottom()))
        self.topWidth.bind(on_press=self.showNumpad)
        self.topHeight.bind(on_press=self.showNumpad)
        self.middleWidth.bind(on_press=self.showNumpad)
        self.middleHeight.bind(on_press=self.showNumpad)
        self.bottomWidth.bind(on_press=self.showNumpad)
        self.bottomHeight.bind(on_press=self.showNumpad)
        self.add_widget(Label(text='top-width'))
        self.add_widget(self.topWidth)
        self.add_widget(Label(text='middle-width'))
        self.add_widget(self.middleWidth)
        self.add_widget(Label(text='bottom-width'))
        self.add_widget(self.bottomWidth)
        self.add_widget(Label(text='top-height'))
        self.add_widget(self.topHeight)
        self.add_widget(Label(text='middle-height'))
        self.add_widget(self.middleHeight)
        self.add_widget(Label(text='bottom-height'))
        self.add_widget(self.bottomHeight)
        self.createPopup()
    
    '''
    set the cross section
    '''
    def setCrossSection(self, crossSection):
        self.cs=crossSection
        self.createGui()
    
    '''
    create the popup
    '''
    def createPopup(self):
        self.numpad=Numpad()
        self.numpad.signInParent(self)
        self.popup=Popup(content=self.numpad)
    
    '''
    open the popup
    '''
    def showNumpad(self,btn):
        self.focusBtn=btn
        self.popup.open()
        
    '''
    set the text of the button
    '''
    def finishedNumpad(self):
        self.focusBtn.text=self.numpad.textinput.text
        self.popup.dismiss()
        value=float(self.focusBtn.text)
        if self.focusBtn==self.topHeight:
            self.cs.setHeightTop(value)
        elif self.focusBtn==self.topWidth:
            self.cs.setWidthTop(value)
        elif self.focusBtn==self.middleHeight:
            self.cs.setHeightMiddle(value)
        elif self.focusBtn==self.middleWidth:
            self.cs.setWidthMiddle(value)
        elif self.focusBtn==self.bottomHeight:
            self.cs.setHeightBottom(value)
        elif self.focusBtn==self.bottomWidth:
            self.cs.setWidthBottom(value)