'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from cross_section_view.doubleT import DoubleT_View
from cross_section_view.aview import AView

class CrossSectionDoubleT(GridLayout, AView): 
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSectionDoubleT, self).__init__(**kwargs)
        self.cols=2
        #topare
        self.tw=0.2
        self.th=0.05
        #middlearea
        self.mw=0.1
        self.heightMiddle=0.05
        #bottomarea
        self.bw=0.3
        self.bh=0.2
        self.view=DoubleT_View()
        self.view.setCrossSection(self)
    
    def getWidthTop(self):
        return self.tw
    
    def setWidthTop(self,value):
        self.tw=value
        self.view.update()
    
    def getHeightTop(self):
        return self.th
    
    def setHeightTop(self,value):
        self.th=value
        self.view.update()
    
    def setWidthMiddle(self,value):
        self.mw=value
        self.view.update()
    
    def getWidthMiddle(self):
        return self.mw
    
    def getHeightMiddle(self):
        return self.heightMiddle
    
    def setHeightMiddle(self,value):
        self.heightMiddle=value
        self.view.update()
    
    def setHeightBottom(self,value):
        self.bh=value
        self.view.update()
    
    def getHeightBottom(self):
        return self.bh
    
    def setWidthBottom(self,value):
        self.bw=value
        self.view.update()
    
    def getWidthBottom(self):
        return self.bw
    
    def getMaxHeight(self):
        return self.th+self.bh+self.heightMiddle
    
    def getMaxWidth(self):
        wmax=self.tw
        if wmax<self.mw:
            wmax=self.mw
        if wmax<self.bw:
            wmax=self.bw
        return wmax
    
    def setInformation(self,information):
        self.information=information
    
    def setAck(self,ack):
        pass
    
    '''
    the method addLayer add new materials in the view
    '''
    def addLayer(self,percent,material):
        self.view.addLayer(percent,material)
    
    def deleteLayer(self):
        self.view.deleteLayer()
    
    def setLayerInformation(self,name,price,density,stiffness,strength,percent):
        self.information.updateLayerInformation(name,price,density,stiffness,strength,percent)
    
    def setCrossSectionInformation(self):
        pass
    
    def getLayers(self):
        return self.view.getLayers()
    
    def setPercent(self, value):
        pass
    
    def calculateWeightPrice(self):
        weight=price=percent_of_layers=0.
        #go trough all layers and get the weight of them
        for l in self.view.layers:
            cur=l.getWeight()
            weight+=cur
            price+=cur*l.material.price
            percent_of_layers+=(l.r1.yrange[1]-l.r1.yrange[0]+l.r2.yrange[1]-l.r2.yrange[0] /\
                                l.r3.yrange[1]-l.r3.yrange[0])/self.cheight
        #if the percent_of_layers is not 1 there is a matrix
        #with concrete as material
        weight+=(1-percent_of_layers)*self.cw*self.concrete_density
        price+=(1-percent_of_layers)*self.cheight*self.cw*self.concrete_price
        self.weight=weight
        self.price=price
    
    def calculateStrength(self):
        pass
    
    def calculateStrainOfConcrete(self):
        pass