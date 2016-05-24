'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionView.doubleTView import DoubleTView
from crossSectionView.aview import AView


class CrossSectionDoubleT(GridLayout, AView):
    # Constructor

    def __init__(self, **kwargs):
        super(CrossSectionDoubleT, self).__init__(**kwargs)
        self.cols = 2
        # topare
        self.tw = 0.2
        self.th = 0.2
        # middlearea
        self.mw = 0.1
        self.mh = 0.05
        # bottomarea
        self.bw = 0.3
        self.bh = 0.2
        self.concreteDensity = 2300.
        self.concretePrice = 0.065
        self.concreteStiffness = 30000.
        self.concreteStrength = 3.
        self.view = DoubleTView()
        self.view.setCrossSection(self)

    '''
    return the top-width
    '''

    def getWidthTop(self):
        return self.tw

    '''
    set the top-width
    '''

    def setWidthTop(self, value):
        self.tw = value
        self.view.update()

    '''
    return the top-height
    '''

    def getHeightTop(self):
        return self.th

    '''
    set the top-height
    '''

    def setHeightTop(self, value):
        self.th = value
        self.view.update()

    '''
    set the middle-width
    '''

    def setWidthMiddle(self, value):
        self.mw = value
        self.view.update()
    '''
    return the middle-width
    '''

    def getWidthMiddle(self):
        return self.mw

    '''
    return the middle-height
    '''

    def getHeightMiddle(self):
        return self.mh

    '''
    set the middle-height
    '''

    def setHeightMiddle(self, value):
        self.mh = value
        self.view.update()

    '''
    set the bottom-height
    '''

    def setHeightBottom(self, value):
        self.bh = value
        self.view.update()

    '''
    return the bottom-height
    '''

    def getHeightBottom(self):
        return self.bh

    '''
    set the bottom-width
    '''

    def setWidthBottom(self, value):
        self.bw = value
        self.view.update()

    '''
    return the bottom-width
    '''

    def getWidthBottom(self):
        return self.bw

    '''
    return the cs-height
    '''

    def getMaxHeight(self):
        return self.th + self.bh + self.mh

    '''
    return the max-width
    '''

    def getMaxWidth(self):
        wmax = self.tw
        if wmax < self.mw:
            wmax = self.mw
        if wmax < self.bw:
            wmax = self.bw
        return wmax

    '''
    set the cs-information
    '''

    def setInformation(self, information):
        self.information = information

    '''
    set the ack
    '''

    def setAck(self, ack):
        pass

    '''
    the method addLayer add new materials in the view
    '''

    def addLayer(self, percent, material):
        self.view.addLayer(percent, material)

    '''
    delete the selected layer
    '''

    def deleteLayer(self):
        self.view.deleteLayer()

    '''
    update the layerinformation in the cs-information
    '''

    def setLayerInformation(self, name, price, density, stiffness, strength, percent):
        self.information.updateLayerInformation(
            name, price, density, stiffness, strength, percent)

    '''
    update the cross section information in the cs-information
    '''

    def setCrossSectionInformation(self):
        pass
        #self.information.updateCrossSectionInformation(self.price, self.weight, self.strength)

    '''
    set the percent
    '''

    def setPercent(self, value):
        self.view.setPercent(value)

    '''
    calculate the weight and price
    '''

    def calculateWeightPrice(self):
        pass
        '''
        weight=price=percentOfLayers=0.
        #go trough all layers and get the weight of them
        for l in self.view.layers:
            cur=l.getWeight()
            weight+=cur
            price+=cur*l.material.price
            percentOfLayers+=l.getHeight()/(self.th+self.mh+self.bh)
        #if the percentOfLayers is not 1 there is a matrix
        #with concrete as material
        weight+=(1-percentOfLayers)*self.cw*self.concreteDensity
        price+=(1-percentOfLayers)*self.cheight*self.cw*self.concretePrice
        self.weight=weight
        self.price=price
        '''

    '''
    calculate the strength of the cross section
    '''

    def calculateStrength(self):
        pass
        '''
        strength=0.
        #cur supremum
        self.minOfMaxstrain=1e10
        #max strain is necessary for other calculations
        self.maxOfMaxstrain=0
        percentOfLayers=0.
        #find the minimum max_strain and the maximum max_strain
        for l in self.view.layers:
            percentOfLayers+=l.getHeight()/(self.th+self.mh+self.bh)
            curStrain=l.getStrain()
            #proof whether the curStrain is smaller as the min
            if curStrain<self.minOfMaxstrain:
                self.minOfMaxstrain=curStrain
            #proof whether the curStrain is bigger as the max
            if curStrain>self.maxOfMaxstrain:
                self.maxOfMaxstrain=curStrain
        #if the percentOfLayers is not 1 there is a matrix
        #with concrete as material
        if 1.-percentOfLayers>0:
            cur_value=self.concreteStrength/self.concreteStiffness
            if self.minOfMaxstrain>cur_value:
                self.minOfMaxstrain=cur_value
            if self.maxOfMaxstrain<cur_value:
                self.maxOfMaxstrain=cur_value
        #calculate the strength
        for l in self.view.layers:
            strength+=self.minOfMaxstrain*l.material.stiffness*l.getHeight()/(self.th+self.mh+self.bh)
        if 1.-percentOfLayers>0:
            strength+=self.minOfMaxstrain*(1.-percentOfLayers)*self.concreteStiffness
        self.strength=strength
        '''
