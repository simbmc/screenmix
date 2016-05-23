'''
Created on 14.03.2016

@author: mkennert
'''


from kivy.garden.graph import Graph, MeshLinePlot
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from itertools import cycle
from cross_section_view.aview import AView
from cross_section_view.layer_rectangle import Layer_Rectangle
from plot.filled_rect import FilledRect
from designClass.design import Design



'''
the class CS_Rectangle_View was developed to show the the cross section,
which has a rectangle shape
'''


class CS_Rectangle_View(BoxLayout, AView):
    # Constructor

    def __init__(self, **kwargs):
        super(CS_Rectangle_View, self).__init__(**kwargs)
        self.cheight = 0.5
        self.cw = 0.25
        self.cs = None
        self.percent_change = False
        self.layers = []
        self.createGraph()
#         self.add_widget(self.updateAllGraph)

    '''
    the method updateAllGraph update the graph. the method should be called, when
    something has changed
    '''
    def updateAllGraph(self):
        for l in self.layers:
            y = l.y
            h = l.h
            l.filledRectCs.xrange =[0., self.cw]
            l.filledRectCs.yrange=[y - h / 2., y + h / 2.]
            if l.focus:
                l.filledRectCs.color = Design.focusColor
            else:
                l.filledRectCs.color=l.colors
        if len(self.layers) == 0:
            self.graph._clear_buffer()
            
    '''
    the method createGraph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def createGraph(self):
        self.graph = Graph(
            #background_color = [1, 1, 1, 1],
            #border_color = [.5,.5,.5,1],
            #tick_color = [0.25,0.25,0.25,1],
            #_trigger_color = [0,0,0,1],
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.cw, ymin=0, ymax=self.cheight)
        self.add_widget(self.graph)

    '''
    the method on_touch_move is invoked after the user touch within a rectangle and move it.
    it changes the position of the rectangle
    '''

    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.cw
        y = (touch.y - y0) / gh * self.cheight
        for l in self.layers:
            if l.focus and l.mouseWithinX(x):
                # case:1 the l don't collide with the border of the cross section
                if y > l.h / 2 and \
                y < self.cheight - l.h / 2:
                    l.setYRange([
                        y - l.h / 2., y + l.h / 2.])
                    l.setYCoordinate(y)
                    return
                # case:2 the l collide with the bottom border of the cross section
                #        the user can't move the l down
                elif y < l.h / 2:
                    l.setYRange([0., l.h])
                    l.setYCoordinate(l.h / 2)
                    return
                # case:3 the l collide with the top border of the cross section
                #       the user can't move the l up
                elif y > self.cheight - l.h / 2:
                    l.setYRange([
                        self.cheight - l.h, self.cheight])
                    l.setYCoordinate(
                        self.cheight - l.h / 2)
                    return

    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''
    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.cw
        y = (touch.y - y0) / gh * self.cheight
        changed = False
        focus = False #one is alreay focus
        for l in self.layers:
            if l.mouseWithin(x, y):
                if l.focus == True and self.percent_change:
                    self.percent_change = False
                    self.updateAllGraph()
                    return
                if l.focus == False and focus == False:
                    l.focus = True
                    focus = True
                    cur_info = l.getMaterialInformations()
                    self.cs.setLayerInformation(cur_info[0], cur_info[1], cur_info[
                                                             2], cur_info[3], cur_info[4], l.h / self.cheight)
                    changed = True
            else:
                if l.focus == True:
                    l.focus = False
                    changed = True
        # update just when something has change
        if changed:
            self.updateAllGraph()

    # not yet so relevant. maybe when we have time, we can finished it
    '''
    def collide(self,x,y,_width,h):
        for rectangle in self.layers:
            if not rectangle.equals(x, y, _width, h):
                #Case:1
                if y+h/2>rectangle.y-rectangle.h/2 and y+h/2<rectangle.y-rectangle.h/2:
                    print('Fall:1')
                    return rectangle.h+h
                #Case:2
                elif y-h/2<rectangle.y+rectangle.h/2 and y+h/2>rectangle.y+rectangle.h/2:
                    print('Fall:2')
                    return -rectangle.h-h
        return 0
    '''

    '''
    the method addLayer was developed to add new layer at the cross section
    '''
    def addLayer(self, value, material):
        height = self.cheight * value
        cur = Layer_Rectangle(self.cw / 2, self.cheight - height / 2., height,
                              self.cw, next(Design.colorcycler), value)
        cur.setMaterial(material)
        y = cur.y
        h = cur.h
        filledRectCs = FilledRect(xrange=[0., self.cw],
                                    yrange=[y - h / 2., y + h / 2.],
                                    color=cur.colors)
        filledRectAck=FilledRect(xrange=[0.,0.],
                                 yrange=[y - h / 2., y + h / 2.],
                                 color=cur.colors)
        self.graph.add_plot(filledRectCs)
        cur.setFilledRectCs(filledRectCs)
        cur.setFilledRectAck(filledRectAck)
        self.layers.append(cur)
        self.updateAllGraph()
        self.cs.calculateStrength()
        self.updateCrossSectionInformation()

    '''
    the method deleteLayer was developed to delete layer from the cross section
    '''

    def deleteLayer(self):
        for layer in self.layers:
            if layer.focus:
                layer.filledRectCs.yrange=[0,0]
                layer.filledRectAck.yrange=[0,0]
                self.layers.remove(layer)
        self.updateAllGraph()
        self.cs.calculateStrength()
        self.updateCrossSectionInformation()

    '''
    the method updateLayerInformation update the layer information of 
    the view_information
    '''
    def updateLayerInformation(self, name, price, density, stiffness, strength, percent):
        self.cs.setLayerInformation(
            name, price, density, stiffness, strength, percent)

    '''
    the method updateCrossSectionInformation update the cross section information of 
    the view_information
    '''
    def updateCrossSectionInformation(self):
        self.cs.calculateWeightPrice()
        self.cs.setCrossSectionInformation()

    '''
    the method getFreePlaces return the free-places, 
    where is no layer
    '''
    def getFreePlaces(self):
        self.free_places = []
        # running index
        cur_y = 0
        # if the cross section contains layers
        if not len(self.layers) == 0:
            while cur_y < self.cheight:
                # layer_exist is a switch to proofs whether
                # a layer exist over the runnning index or not
                layer_exist = False
                min_value = self.cheight
                for layer in self.layers:
                    if layer.y >= cur_y and layer.y < min_value:
                        layer_exist = True
                        min_value = layer.y - layer.h / 2.
                        nextMinValue = layer.y + layer.h / 2.
                        # if the running index is equals the min, means that there's no
                        # area
                        if not cur_y == min_value:
                            self.free_places.append((cur_y, min_value))
                        cur_y = nextMinValue
                # if no layer exist over the running index then that's the last
                # area which is free.
                if not layer_exist:
                    self.free_places.append((cur_y, self.cheight))
                    return self.free_places
        # if no layer exist,all area of the cross section is free
        else:
            self.free_places.append((0, self.cheight))
        return self.free_places

    ##########################################################################
    #                                Setter && Getter                        #
    ##########################################################################
    '''
    the method setPercent change the percent shape of the selected rectangle
    '''
    def setPercent(self, value):
        self.percent_change = True
        for rectangle in self.layers:
            if rectangle.focus:
                rectangle.setHeight(self.cheight * value)
                rectangle.setPercentage(value)
                self.updateAllGraph()
                self.cs.calculateStrength()
                self.updateCrossSectionInformation()
                return

    '''
    the method setHeight change the height of the cross section shape
    and update the layers
    '''
    def setHeight(self, value):
        for l in self.layers:
            l.setYCoordinate(
                l.y / self.cheight * value)
            l.setHeight(
                l.h / self.cheight * value)
            self.updateAllGraph()
        self.cheight = value
        self.graph.ymax = self.cheight
        self.updateCrossSectionInformation()

    '''
    the method setWidth change the width of the cross section shape
    and update the layers
    '''
    def setWidth(self, value):
        self.cw = value
        self.graph.xmax = self.cw
        for rectangle in self.layers:
            rectangle.setWidth(value)
        self.updateAllGraph()
        self.updateCrossSectionInformation()

    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''
    def setCrossSection(self, cross_section):
        self.cs = cross_section

    '''
    return all layers 
    '''
    def getLayers(self):
        return self.layers
