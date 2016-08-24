'''
Created on 14.03.2016
@author: mkennert
'''

import copy

from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

from crossSectionView.iView import IView
from layers.rectLayer import RectLayer
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.filled_rect import FilledRect
from plot.dashedLine import DashedLine


class RectView(BoxLayout, IView):
    
    '''
    the class RectView was developed to show the rectangle-shape of 
    the cross-section
    '''
    
    # important components
    cs = ObjectProperty()
    
    # width, height of the cross section
    w, h = NumericProperty(0.25), NumericProperty(0.5)
    
    # strings
    ylabelStr = StringProperty('cross-section-height [m]')
    xlabelStr = StringProperty('cross-section-width [m]')
    
    # constructor
    def __init__(self, **kwargs):
        super(RectView, self).__init__(**kwargs)
        self.create_graph()
        
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning.
    '''

    def create_graph(self):
        self.graph = OwnGraph(xlabel=self.xlabelStr, ylabel=self.ylabelStr,
                              x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True,
                              xmin=0, xmax=self.w, ymin=0, ymax=self.h)
        self.add_widget(self.graph)

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, value, material):
        h = self.h * value  # value is the percent of the layer
        y = self.h - h / 2.  # y-coordinate
        cur = RectLayer(self.w / 2, y, h, self.w, material.color, value)
        cur.material = material
        cur.strain = material.strength / material.stiffness
        # if the value is too small to see a rectangle
        # => use dashed line
        if value < 0.01:
            cur.layerCs = DashedLine(color=[255, 0, 0],
                                   points=[(0, y), (self.w, y)])
            cur.layerAck = DashedLine(color=[255, 0, 0],
                                   points=[(0, y), (self.w, y)])
        else:
            # create the filled-rect for the cs-view and the ack-right.
            cur.layerCs = FilledRect(xrange=[0., self.w], color=cur.colors,
                                      yrange=[y - h / 2., y + h / 2.])
            cur.layerAck = FilledRect(xrange=[0., 0.], color=cur.colors,
                                       yrange=[y - h / 2., y + h / 2.])
        self.graph.add_plot(cur.layerCs)
        # safe the layer in the cross-section-layers-list 
        self.cs.layers.append(cur) 
        self.update_all_graph()
        self.update_cs_information()
        
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        # if the cross-section has no layer, 
        # there's nothing to do
        if not self.cs.layers:
            return
        for layer in self.cs.layers:
            if layer.focus:
                if layer.p > 0.01:
                    layer.layerCs.yrange = [0, 0]
                    layer.layerAck.yrange = [0, 0]
                else:
                    layer.layerAck.points = []
                    layer.layerCs.points = []
                self.cs.layers.remove(layer)
        self.update_all_graph()
        # update the cs-information
        self.update_cs_information()

    '''
    the method get_free_places return the free-places, 
    where is no layer
    '''

    def get_free_places(self):
        self.free_places = []  # reset the free_places 
        layers = copy.deepcopy(self.cs.layers)
        # if the cross section contains layers
        if self.cs.layers:
            y = 0.  # running index
            self.switch = 1
            while self.switch > 0:
                minValue = self.h
                cur = self.findMin(layers)
                if self.switch > 0:
                    minValue = cur.y - cur.h / 2.
                    nextMinValue = cur.y + cur.h / 2.
                    self.free_places.append((y, minValue))
                    y = nextMinValue
            self.free_places.append((y, self.h))
            return self.free_places
        # if no layer exist,all area of the cross section is free
        else:
            self.free_places.append((0, self.h))
        return self.free_places

    '''
    find the layer which is the lowest
    '''

    def findMin(self, layers):
        # if the layers-list don't contains layers
        # change the switch of the method get-free-places
        if not layers:
            self.switch = -1
        else:
            # for the beginning minY=cross-section-height
            minY = self.h
            for layer in layers:
                y = layer.y - layer.h / 2.
                if y < minY:
                    minY = y
                    cur = layer
            layers.remove(cur)
            return cur
        
    '''
    the method update_percent change the percent shape of the selected rectangle
    '''

    def update_percent(self, value):
        for layer in self.cs.layers:
            if layer.focus:
                if layer.p > 0.01 and value < 0.01:
                    layer.h, layer.p = self.h * value, value
                    self.graph.remove_plot(layer.layerCs)
                    layer.h, layer.p = self.h * value, value
                    self.graph.remove_plot(layer.layerCs)
                    layer.layerCs = DashedLine(color=[255, 0, 0],
                                   points=[(0, layer.y), (self.w, layer.y)])
                    layer.layerAck = DashedLine(color=[255, 0, 0],
                                   points=[(0, layer.y), (self.w, layer.y)])
                    self.graph.add_plot(layer.layerCs)
                elif layer.p < 0.01 and value > 0.01:
                    layer.h, layer.p = self.h * value, value
                    self.graph.remove_plot(layer.layerCs)
                    layer.layerCs = DashedLine(color=[255, 0, 0],
                                   points=[(0, layer.y), (self.w, layer.y)])
                    layer.layerAck = DashedLine(color=[255, 0, 0],
                                   points=[(0, layer.y), (self.w, layer.y)])
                    layer.h, layer.p = self.h * value, value
                    self.graph.remove_plot(layer.layerCs)
                    layer.layerCs = FilledRect(xrange=[0., self.w], color=layer.colors,
                                      yrange=[layer.y - layer.h / 2., layer.y + layer.h / 2.])
                    layer.layerAck = FilledRect(xrange=[0., 0.], color=layer.colors,
                                       yrange=[layer.y - layer.h / 2., layer.y + layer.h / 2.])
                    self.graph.add_plot(layer.layerCs)
                else:
                    layer.h, layer.p = self.h * value, value
                self.cs.calculate_weight_price()
                self.cs.calculate_strength()
                self.update_cs_information()
                self.cs.refEdit.lblRatio.text = str(layer.p * 100)
                self.update_all_graph()
                return

    '''
    the method update_height change the height of the cross section shape
    and update the layers
    '''

    def update_height(self, value):
        # a is the scalar to scale the layers
        a, self.h = value / self.h, value
        for layer in self.cs.layers:
            layer.y, layer.h = layer.y * a, layer.h * a
        self.update_all_graph()
        # update the graph-height 
        self.graph.ymax = self.h
        self.graph.y_ticks_major = self.h / 5.
        # update the information of the cross section
        self.update_cs_information()

    '''
    the method update_width change the width of the cross section shape
    and update the layers
    '''

    def update_width(self, value):
        self.w = value
        for layer in self.cs.layers:
            layer.w = value
        self.update_all_graph()
        # update the graph-width
        self.graph.xmax = self.w
        self.graph.x_ticks_major = self.w / 5.
        # update the information of the cross section
        self.update_cs_information()
    
    '''
    update the layers in the graph.    
    '''

    def update_all_graph(self):
        for layer in self.cs.layers:
            # update the height and the width of the layers
            y, h = layer.y, layer.h
            if layer.p > 0.01:
                layer.layerCs.xrange = [0., self.w]
                layer.layerCs.yrange = [y - h / 2., y + h / 2.]
                layer.layerAck.yrange = [y - h / 2., y + h / 2.]
            else:
                print(layer)
                layer.layerAck.points = [(0, y), (self.w, y)]
                layer.layerCs.points = [(0, y), (self.w, y)]
            # update the focus-color
            if layer.focus:
                layer.layerCs.color = Design.focusColor
            else:
                layer.layerCs.color = layer.colors
        if len(self.cs.layers) == 0:
            self.graph._clear_buffer()
        
    '''
    the method on_touch_move is invoked after the user touch within a rectangle and move it.
    it changes the position of the rectangle
    '''

    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.w
        y = (touch.y - y0) / gh * self.h
        for layer in self.cs.layers:
            if layer.focus and layer.mouse_within_x(x):
                # when the layer is just a dashed line
                if layer.p < 0.01:
                    layer.layerAck.points = [(0, y), (self.w, y)]
                    layer.layerCs.points = [(0, y), (self.w, y)]
                    layer.y = y
                    return
                # case:1 the layer don't collide with the border of the cross
                # section
                if y > layer.h and y < self.h :
                    layer.update_yrange([
                        y - layer.h, y ])
                    layer.y = y - layer.h / 2.
                    return
                # case:2 the layer collide with the bottom border of the cross section
                #       the user can't move the layer down
                elif y < layer.h:
                    layer.update_yrange([0., layer.h])
                    layer.y = layer.h / 2.
                    return
                # case:3 the layer collide with the top border of the cross section
                #       the user can't move the layer up
                elif y > self.h - layer.h / 2.:
                    layer.update_yrange([
                        self.h - layer.h, self.h])
                    layer.y = self.h - layer.h / 2.
                    return

    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.w
        y = (touch.y - y0) / gh * self.h
        # change is a switch to make sure, that the view just update,
        # when something has changed
        changed = False
        layerFocus = False
        for layer in self.cs.layers:
            # if the touch is in the layer
            if layer.mouse_within(x, y, self.h / 50.):
                layerFocus = True
                # when the layer has already the focus
                if layer.focus:
                    self.update_all_graph()
                    return
                # when the layer has not the focus
                if not layer.focus:
                    layer.focus = True
                    cur = layer.get_material_informations()
                    self.cs.update_layer_information(cur[0], cur[1], cur[
                        2], cur[3], cur[4], layer.h / self.h)
                    changed = True
            # if the touch is not in the layer and the the layer has the focus then
            # the focus disappears
            else:
                if layer.focus:
                    layer.focus = False
                    changed = True
        # update just when something has change
        if changed:
            self.update_all_graph()
        if not layerFocus:
            self.cs.reset_layer_information()
