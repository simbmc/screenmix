'''
Created on 09.05.2016

@author: mkennert
'''
from kivy.uix.gridlayout import GridLayout

from crossSectionView.aview import AView
from designClass.design import Design
from kivy.garden.graph import Graph, MeshLinePlot
from layers.layerDoubleT import LayerDoubleT
from plot.filled_rect import FilledRect


class DoubleTView(AView, GridLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(DoubleTView, self).__init__(**kwargs)
        AView.__init__(self)
        self.cols = 1
        self.layers = []
    '''
    the method createGraph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def createGraph(self):
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.wmax + self.deltaX,
            ymin=0, ymax=self.hmax + self.deltaY)
        self.add_widget(self.graph)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawDoubleT()
        self.graph.add_plot(self.p)

    '''
    draw the double_T
    '''

    def drawDoubleT(self):
        x0 = self.graph.xmax / 2.
        y1 = 0
        x1 = x0 - self.bw / 2.
        y2 = y3 = self.bh
        x3 = x1 + self.bw / 2. - self.mw / 2.
        y4 = y3 + self.mh
        x5 = x3 + self.mw / 2. - self.tw / 2.
        y6 = y4 + self.th
        x7 = x5 + self.tw
        x9 = x7 - self.tw / 2. + self.mw / 2.
        x11 = x9 + self.bw / 2. - self.mw / 2.
        return [(x1, y1), (x1, y2), (x3, y2), (x3, y4), (x5, y4), (x5, y6),
                (x7, y6), (x7, y4), (x9, y4), (x9, y3), (x11, y3), (x11, y1)]

    '''
    update the view when the model has changed
    '''

    def update(self):
        # save old values for the update
        self.obw = self.bw
        self.obh = self.bh
        self.omw = self.mw
        self.omh = self.mh
        self.otw = self.tw
        self.oth = self.th
        self.ohmax = self.hmax
        # get the new values
        self.bh = self.cs.getHeightBottom()
        self.bw = self.cs.getWidthBottom()
        self.mh = self.cs.getHeightMiddle()
        self.mw = self.cs.getWidthMiddle()
        self.th = self.cs.getHeightTop()
        self.tw = self.cs.getWidthTop()
        self.hmax = self.cs.getMaxHeight()
        self.wmax = self.cs.getMaxWidth()
        # update graph
        self.updateAllGraph()

    '''
    set the percent of the selected layer
    '''

    def setPercent(self, value):
        for l in self.layers:
            if l.r1.color == Design.focusColor:
                l.percent = value
                op = l.getHeight() / (self.th + self.mh + self.bh)
                a = value / op
                delta = self.wmax / 2. + self.deltaX / 2.
                print(l.r1.yrange[1])
                # l.r1.yrange[0]+=a.*l.r1.yrange[0]
                # l.r1.yrange[1]+=a*l.r1.yrange[1]
                # l.r2.yrange[0]=a*l.r2.yrange[0]
                # l.r2.yrange[1]=a*l.r2.yrange[1]
                # l.r3.yrange[0]=a*l.r3.yrange[0]
                # l.r3.yrange[1]=a*l.r3.yrange[1]
                l.h1 = a * l.h1
                l.h2 = a * l.h2
                l.h3 = a * l.h3
                # case 1
                if l.r1.yrange[1] < self.bh:
                    print('case 1')
                    x = delta - self.bw / 2.
                    l.r1.xrange = [x, x + self.bw]
                    l.r2.xrange = [x, x + self.bw]
                    l.r3.xrange = [x, x + self.bw]
                    l.r1.yrange[0] = a * l.r1.yrange[0]
                    l.r1.yrange[1] = a * l.r1.yrange[1]
                    l.r2.yrange[0] = a * l.r2.yrange[0]
                    l.r2.yrange[1] = a * l.r2.yrange[1]
                    l.r3.yrange = [0, 0]
                # case 2
                elif l.r1.yrange[1] < self.bh + self.mh and l.r2.yrange[0] > self.bh:
                    print('case 2')
                    x = delta - self.mw / 2.
                    l.r1.xrange = [x, x + self.mw]
                    l.r2.xrange = [x, x + self.mw]
                    l.r1.yrange[0] = a * l.r1.yrange[0]
                    l.r1.yrange[1] = a * l.r1.yrange[1]
                    l.r2.yrange[0] = a * l.r2.yrange[0]
                    l.r2.yrange[1] = a * l.r2.yrange[1]
                    l.r3.yrange = [0, 0]
                # case 3
                elif l.r2.yrange[0] > self.bh + self.mh:
                    print('case 3')
                    x = delta - self.tw / 2.
                    l.r1.xrange = [x, x + self.tw]
                    l.r2.xrange = [x, x + self.tw]
                    l.r3.xrange = [x, x + self.tw]
                    l.r1.yrange[0] = a * l.r1.yrange[0]
                    l.r1.yrange[1] = a * l.r1.yrange[1]
                    l.r2.yrange[0] = a * l.r2.yrange[0]
                    l.r2.yrange[1] = a * l.r2.yrange[1]
                    l.r3.yrange = [0, 0]
                # case 4
                elif l.r1.yrange[1] < self.bh + self.mh and l.r2.yrange[0] < self.bh:
                    print('case 4')
                    x1 = delta - self.mw / 2.
                    x2 = delta - self.bw / 2.
                    l.r1.yrange = [self.bh, self.bh + l.h1 / 2.]
                    l.r1.xrange = [x1, x1 + self.mw]
                    l.r2.xrange = [x2, x2 + self.bw]
                    l.r2.yrange = [self.bh - l.h1 / 2., self.bh]
                    l.r3.yrange = [0, 0]
                # case 5
                elif l.r1.yrange[1] > self.bh + self.mh and l.r2.yrange[0] < self.bh + self.mh and l.r2.yrange[0] > self.bh:
                    print('case 5')
                    x1 = delta - self.tw / 2.
                    x2 = delta - self.mw / 2.
                    l.r1.yrange = [
                        self.bh + self.mh, self.bh + self.mh + l.h1 / 2.]
                    l.r1.xrange = [x1, x1 + self.tw]
                    l.r2.xrange = [x2, x2 + self.mw]
                    l.r2.yrange = [
                        self.bh + self.mh - l.h1 / 2., self.bh + self.mh]
                    l.r3.yrange = [0, 0]
                # case 6
                else:
                    print('case 6')
                    x1 = delta - self.tw / 2.
                    x2 = delta - self.mw / 2.
                    x3 = delta - self.bw / 2.
                    l.r1.yrange = [
                        self.bh + self.mh, self.bh + self.mh + l.h1 / 2.]
                    l.r2.yrange = [self.bh, self.bh + self.mh]
                    l.r3.yrange = [self.bh - (l.h1 / 2.), self.bh]
                    l.r1.xrange = [x1, x1 + self.tw]
                    l.r2.xrange = [x2, x2 + self.mw]
                    l.r3.xrange = [x3, x3 + self.bw]

    '''
    the method addLayer was developed to add new layer at the cross section
    '''

    def addLayer(self, value, material):
        h = self.hmax * value
        h1 = self.th
        tw = self.tw
        mw = self.mw
        # Case 1
        # Falls das Layer prozentual gesehen in dem Top-Area passt
        if h <= self.th:
            print('case 1')
            lx = self.wmax / 2. - self.tw / 2. + self.deltaX
            l = LayerDoubleT(h, 0, 0,
                             self.tw, self.tw, 0,
                             next(Design.colorcycler), value)
            l.setMaterial(material)
            y1 = self.hmax - h / 2.
            h1 = l.h1
            r1 = FilledRect(xrange=[lx - self.deltaX / 2., self.tw + lx - self.deltaX / 2.],
                            yrange=[y1 - h1 / 2., y1 + h1 / 2.],
                            color=l.colors)
            y2 = self.hmax - h / 2.
            h2 = l.h2
            r2 = FilledRect(xrange=[lx - self.deltaX / 2., self.tw + lx - self.deltaX / 2.],
                            yrange=[
                                y2 - l.h2 / 2. - self.deltaY, y2 + l.h2 / 2. - self.deltaY],
                            color=l.colors)
            r3 = FilledRect(xrange=[0, 0],
                            yrange=[0, 0],
                            color=l.colors)
        # Case 2:
        # Falls das Layer nicht im toparea, aber im toparea+middlearea passt
        elif h <= self.th + self.mh:
            print('case 2')
            lx1 = self.wmax / 2. - tw / 2. + self.deltaX
            lx2 = self.wmax / 2. - mw / 2. + self.deltaX
            ly1 = self.hmax - h1 / 2.
            h2 = h - h1
            ly2 = ly1 - self.th / 2. - h2 / 2.
            l = LayerDoubleT(
                h1, h2, 0,
                self.tw, self.mw, 0,
                next(Design.colorcycler), value)
            l.setMaterial(material)
            h1 = l.h1
            r1 = FilledRect(xrange=[lx1 - self.deltaX / 2.,
                                    self.tw + lx1 - self.deltaX / 2.],
                            yrange=[ly1 - h1 / 2.,
                                    ly1 + h1 / 2.],
                            color=l.colors)
            h2 = l.h2
            r2 = FilledRect(xrange=[lx2 - self.deltaX / 2.,
                                    self.mw + lx2 - self.deltaX / 2.],
                            yrange=[ly2 - h2 / 2., ly2 + h2 / 2.],
                            color=l.colors)
            r3 = FilledRect(xrange=[0, 0],
                            yrange=[0, 0],
                            color=l.colors)
        # case 3
        # Falls das Layer nicht im toparea and middlearea passt
        else:
            print('case 3')
            lx1 = self.wmax / 2. - self.tw / 2. + self.deltaX
            lx2 = self.wmax / 2. - self.mw / 2. + self.deltaX
            lx3 = self.wmax / 2. - self.bw / 2. + self.deltaX / 2.
            h2 = self.mh
            h3 = h - h1 - h2
            ly1 = self.hmax - h1 / 2.
            ly2 = ly1 - h1 / 2. - h2 / 2.
            ly3 = ly2 - h2 / 2. - h3
            l = LayerDoubleT(
                h1 + h3 / 2., h2 + h3 / 2., 0,
                self.tw, self.mw, self.bw,
                next(Design.colorcycler), value)
            l.setMaterial(material)
            r1 = FilledRect(xrange=[lx1 - self.deltaX / 2., self.tw + lx1 - self.deltaX / 2.],
                            yrange=[ly1 - h1 / 2., ly1 + h1 / 2.], color=l.colors)
            r2 = FilledRect(xrange=[lx2 - self.deltaX / 2., self.mw + lx2 - self.deltaX / 2.],
                            yrange=[ly2 - h2 / 2., ly2 + h2 / 2.], color=l.colors)
            r3 = FilledRect(xrange=[lx3, lx3 + self.bw],
                            yrange=[ly3, ly3 + h3], color=l.colors)
        l.setFilledRect1(r1)
        l.setFilledRect2(r2)
        l.setFilledRect3(r3)
        self.graph.add_plot(r1)
        self.graph.add_plot(r2)
        self.graph.add_plot(r3)
        self.layers.append(l)
        self.cs.calculateStrength()
        self.updateCrossSectionInformation()

    '''
    update the graph and the layers
    '''

    def updateAllGraph(self):
        # update graph
        self.deltaX = self.wmax / 10.
        self.deltaY = self.hmax / 50.
        self.graph.xmax = self.wmax + self.deltaX
        self.graph.ymax = self.hmax + self.deltaY
        self.graph.x_ticks_major = self.graph.xmax / 5.
        self.graph.y_ticks_major = self.graph.ymax / 5.
        self.graph.remove_plot(self.p)
        self.p = MeshLinePlot(color=[1, 1, 1, 1])
        self.p.points = self.drawDoubleT()
        self.graph.add_plot(self.p)
        # update layers
        self.updateWidth()
        self.updateHeight()

    '''
    update the width of the layer
    '''

    def updateWidth(self):
        delta = self.wmax / 2. + self.deltaX / 2.
        for l in self.layers:
            if not l.w1 == self.obw:
                l.w1 = self.bw
                l.r1.xrange = [delta - self.bw / 2., delta + self.bw / 2.]
            elif not l.w1 == self.omw:
                l.w1 = self.mw
                l.r1.xrange = [delta - self.mw / 2., delta + self.mw / 2.]
            elif not l.w1 == self.otw:
                l.w1 = self.tw
                l.r1.xrange = [delta - self.tw / 2., delta + self.tw / 2.]
            if not l.w2 == self.obw:
                l.w2 = self.bw
                l.r2.xrange = [delta - self.bw / 2., delta + self.bw / 2.]
            elif not l.w2 == self.omw:
                l.w2 = self.mw
                l.r2.xrange = [delta - self.mw / 2., delta + self.mw / 2.]
            elif not l.w2 == self.otw:
                l.w2 = self.tw
                l.r2.xrange = [delta - self.tw / 2., delta + self.tw / 2.]
            if not l.w3 == self.obw:
                l.w3 = self.bw
                l.r3.xrange = [delta - self.bw / 2., delta + self.bw / 2.]
            elif not l.w3 == self.omw:
                l.w3 = self.mw
                l.r3.xrange = [delta - self.mw / 2., delta + self.mw / 2.]
            elif not l.w3 == self.otw:
                l.w3 = self.tw
                l.r3.xrange = [delta - self.tw / 2., delta + self.tw / 2.]

    '''
    update the height of the layers
    '''

    def updateHeight(self):
        delta = self.wmax / 2. + self.deltaX / 2.
        a = self.hmax / self.ohmax
        for l in self.layers:
            # l.r1.yrange[0]=a*l.r1.yrange[0]
            l.r1.yrange[1] = a * l.r1.yrange[1]
            # l.r2.yrange[0]=a*l.r2.yrange[0]
            l.r2.yrange[1] = a * l.r2.yrange[1]
            # l.r3.yrange[0]=a*l.r3.yrange[0]
            l.r3.yrange[1] = a * l.r3.yrange[1]
            # l.h1=a*l.h1
            # l.h2=a*l.h2
            # l.h3=a*l.h3
            print('h1: ' + str(l.h1))
            print('h2: ' + str(l.h1))
            print('h3: ' + str(l.h1))
            # case 1
            if l.r1.yrange[1] < self.bh:
                print('case 1')
                x = delta - self.bw / 2.
                l.r1.xrange = [x, x + self.bw]
                l.r2.xrange = [x, x + self.bw]
                l.r3.xrange = [x, x + self.bw]
            # case 2
            elif l.r1.yrange[1] < self.bh + self.mh and l.r2.yrange[0] > self.bh:
                print('case 2')
                x = delta - self.mw / 2.
                l.r1.xrange = [x, x + self.mw]
                l.r2.xrange = [x, x + self.mw]
            # case 3
            elif l.r2.yrange[0] > self.bh + self.mh:
                print('case 3')
                x = delta - self.tw / 2.
                l.r1.xrange = [x, x + self.tw]
                l.r2.xrange = [x, x + self.tw]
                l.r3.xrange = [x, x + self.tw]
            # case 4
            elif l.r1.yrange[1] < self.bh + self.mh and l.r2.yrange[0] < self.bh:
                print('case 4')
                x1 = delta - self.mw / 2.
                x2 = delta - self.bw / 2.
                l.r1.xrange = [x1, x1 + self.mw]
                l.r1.yrange = [self.bh, self.bh + l.h1 / 2.]
                l.r2.xrange = [x2, x2 + self.bw]
                l.r2.yrange = [self.bh - l.h1 / 2., self.bh]
            # case 5
            elif l.r1.yrange[1] > self.bh + self.mh and l.r2.yrange[0] < self.bh + self.mh and l.r2.yrange[0] > self.bh:
                print('case 5')
                x1 = delta - self.tw / 2.
                x2 = delta - self.mw / 2.
                l.r1.yrange = [
                    self.bh + self.mh, self.bh + self.mh + l.h1 / 2.]
                l.r1.xrange = [x1, x1 + self.tw]
                l.r2.xrange = [x2, x2 + self.mw]
                l.r2.yrange = [
                    self.bh + self.mh - l.h1 / 2., self.bh + self.mh]
            # case 6
            else:
                print('case 6')
                x1 = delta - self.tw / 2.
                x2 = delta - self.mw / 2.
                x3 = delta - self.bw / 2.
                l.r1.yrange = [
                    self.bh + self.mh, self.bh + self.mh + l.h1 / 2.]
                l.r2.yrange = [self.bh, self.bh + self.mh]
                l.r3.yrange = [self.bh - (l.h1 / 2.), self.bh]
                l.r1.xrange = [x1, x1 + self.tw]
                l.r2.xrange = [x2, x2 + self.mw]
                l.r3.xrange = [x3, x3 + self.bw]

    '''
    return the freePlaces, where is no layer of the cross section
    '''

    def getFreePlaces(self):
        pass

    '''
    update the cross section information
    '''

    def updateCrossSectionInformation(self):
        self.cs.calculateWeightPrice()
        self.cs.setCrossSectionInformation()

    '''
    delete the selected layer
    '''

    def deleteLayer(self):
        for l in self.layers:
            if l.r1.color == Design.focusColor:
                l.h1 = l.h2 = l.h3 = 0
                l.r1.yrange = l.r2.yrange = l.r3.yrange = [0, 0]
                self.layers.remove(l)
    '''
    update the layer information in the information-area
    '''

    def updateLayerInformation(self, name, price, density, stiffness, strength, percent):
        self.cs.setLayerInformation(name, price, density,
                                    stiffness, strength, percent)

    '''
    the method on_touch_move is invoked after the user touch within a rectangle and move it.
    it changes the position of the rectangle
    '''

    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        y = (touch.y - y0) / gh * self.hmax
        x = (touch.x - x0) / gw * self.wmax
        delta = self.wmax / 2. + self.deltaX / 2.
        for l in self.layers:
            # select the l which has the focus
            if l.mouseWithinX(x) and l.r1.color == Design.focusColor:
                # case 1
                if y + l.h1 > self.hmax:
                    return
                # case 2
                elif y - l.h2 < 0:
                    return
                # case 3
                elif y + l.h1 > self.bh + self.mh and y - l.h2 < self.bh:
                    print('move case 3')
                    x1 = delta - self.tw / 2.
                    l.setXRange1([x1, x1 + self.tw])
                    l.setYRange1([self.bh + self.mh, y + l.h1])
                    x2 = delta - self.mw / 2.
                    l.setXRange2([x2, x2 + self.mw])
                    l.setYRange2(
                        [self.hmax - self.th - self.mh, self.hmax - self.th])
                    x3 = delta - self.bw / 2.
                    l.setXRange3([x3, x3 + self.bw])
                    l.w3 = self.bw
                    l.setYRange3([y - l.h2, self.bh])
                    l.w1 = self.tw
                    l.w2 = self.mw
                    l.w3 = self.bw
                    return
                # case 4
                elif y - l.h2 < self.bh and y + l.h1 > self.bh:
                    print('move case 4')
                    l.setXRange1([delta - self.mw / 2., delta + self.mw / 2.])
                    l.setXRange2([delta - self.bw / 2., delta + self.bw / 2.])
                    height2 = self.bh - y - l.h2 / 2.
                    height1 = -self.bh + y + l.h1
                    print('h1: ' + str(height1))
                    print('h2: ' + str(height2))
                    l.setYRange1([self.bh, self.bh + height1])
                    print('yrange: ' + str(l.r1.yrange))
                    l.setYRange2([y - l.h2, self.bh])
                    l.setYRange3([0, 0])
                    l.w1 = self.mw
                    l.w2 = self.bw
                    l.w3 = 0
                    return
                # case 5
                elif y + l.h1 > self.bh + self.mh and \
                        y - l.h2 < self.bh + self.mh:
                    print('move case 5')
                    l.setXRange1([delta - self.tw / 2., delta + self.tw / 2.])
                    l.setXRange2([delta - self.mw / 2., delta + self.mw / 2.])
                    height1 = y + l.h1 - self.bh - self.mh
                    height2 = l.h1 + l.h2 - height1
                    l.setYRange1(
                        [self.bh + self.mh, self.bh + self.mh + height1])
                    l.setYRange2([y - l.h2, self.bh + self.mh])
                    l.setYRange3([0, 0])
                    l.w1 = self.tw
                    l.w2 = self.mw
                    l.w3 = 0
                    return
                # case 6
                else:
                    print('move case 6')
                    l.setYRange1([y, y + l.h1])
                    l.setYRange2([y - l.h2, y])
                    #l.setYRange3([0, 0])
                    if y < self.bh:
                        l.setXRange1(
                            [delta - self.bw / 2., delta + self.bw / 2.])
                        l.setXRange2(
                            [delta - self.bw / 2., delta + self.bw / 2.])
                        l.w1 = self.bw
                        l.w2 = self.bw
                    elif y < self.bh + self.mh:
                        l.setXRange1(
                            [delta - self.mw / 2., delta + self.mw / 2.])
                        l.setXRange2(
                            [delta - self.mw / 2., delta + self.mw / 2.])
                        l.w1 = self.mw
                        l.w2 = self.mw
                    elif y < self.bh + self.mh + self.th:
                        l.setXRange1(
                            [delta - self.tw / 2., delta + self.tw / 2.])
                        l.setXRange2(
                            [delta - self.tw / 2., delta + self.tw / 2.])
                        l.w1 = self.tw
                        l.w2 = self.tw
                    print('x0: '+str(x))
                    print('middle1: '+str(l.w1))
                    print('middle2: '+str(l.w2))
                    print('middle3: '+str(l.w3))
                    return

    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        y = (touch.y - y0) / gh * self.hmax
        x = (touch.x - x0) / gw * self.wmax
        changed = False
        for l in self.layers:
            if l.mouseWithin(x, y) and changed == False:
                changed = True
                l.setColor(Design.focusColor)
                info = l.getMaterialInformations()
                self.updateLayerInformation(info[0], info[1],
                                            info[2], info[3],
                                            info[4], l.percent)
            else:
                l.resetColor()

    '''
    set the cross section
    '''

    def setCrossSection(self, crossSection):
        self.cs = crossSection
        self.bh = self.cs.getHeightBottom()
        self.bw = self.cs.getWidthBottom()
        self.mh = self.cs.getHeightMiddle()
        self.mw = self.cs.getWidthMiddle()
        self.th = self.cs.getHeightTop()
        self.tw = self.cs.getWidthTop()
        self.hmax = self.cs.getMaxHeight()
        self.wmax = self.cs.getMaxWidth()
        self.createGraph()
