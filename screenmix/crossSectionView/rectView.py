'''
Created on 14.03.2016
@author: mkennert
'''

import copy

from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from crossSectionView.iView import IView
from layers.rectLayer import RectLayer
from ownComponents.design import Design
from ownComponents.ownGraph import OwnGraph
from plot.filled_rect import FilledRect


class RectView(BoxLayout, IView):
    '''
    the class RectView was developed to show the the cross section,
    which has a rectangle shape
    '''
    cs = ObjectProperty()
    w, h = NumericProperty(0.25), NumericProperty(0.5)
    
    # constructor

    def __init__(self, **kwargs):
        super(RectView, self).__init__(**kwargs)
        self.percentChange = False
        self.create_graph()
        
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = OwnGraph(x_ticks_major=0.05, y_ticks_major=0.05,
                              y_grid_label=True, x_grid_label=True,
                            xmin=0, xmax=self.w, ymin=0, ymax=self.h)
        self.add_widget(self.graph)
    
    '''
    update the layers in the graph
    '''

    def update_all_graph(self):
        for layer in self.cs.layers:
            y, h = layer.y, layer.h
            layer.layerCs.xrange = [0., self.w]
            layer.layerCs.yrange = [y - h / 2., y + h / 2.]
            layer.layerAck.yrange = [y - h / 2., y + h / 2.]
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
        changed = False
        curFocus = False
        for layer in self.cs.layers:
            if layer.mouse_within(x, y):
                if layer.focus == True and self.percentChange:
                    self.percentChange = False
                    self.update_all_graph()
                    return
                if layer.focus == False and curFocus == False:
                    layer.focus = True
                    curFocus = True
                    cur = layer.get_material_informations()
                    self.cs.update_layer_information(cur[0], cur[1], cur[
                        2], cur[3], cur[4], layer.h / self.h)
                    changed = True
            else:
                if layer.focus == True:
                    layer.focus = False
                    changed = True
        # update just when something has change
        if changed:
            self.update_all_graph()

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, value, material):
        h = self.h * value
        y = self.h - h / 2.
        cur = RectLayer(self.w / 2, y, h,
                        self.w, material.color, value)
        cur.material = material
        cur.layerCs = FilledRect(xrange=[0., self.w],
                                  yrange=[y - h / 2., y + h / 2.],
                                  color=cur.colors)
        cur.layerAck = FilledRect(xrange=[0., 0.],
                                   yrange=[y - h / 2., y + h / 2.],
                                   color=cur.colors)
        self.graph.add_plot(cur.layerCs)
        self.cs.layers.append(cur)
        self.update_all_graph()
        self.update_cs_information()
        
    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        if len(self.cs.layers) == 0:
            return
        for layer in self.cs.layers:
            if layer.focus:
                layer.layerCs.yrange = [0, 0]
                layer.layerAck.yrange = [0, 0]
                self.cs.layers.remove(layer)
        self.update_all_graph()
        self.cs.calculate_strength()
        self.update_cs_information()

    '''
    the method update_cs_information update the cross section information of 
    the view_information
    '''

    def update_cs_information(self):
        self.cs.calculate_weight_price()
        self.cs.update_cs_information()

    '''
    the method get_free_places return the free-places, 
    where is no layer
    '''

    def get_free_places(self):
        self.free_places = []
        layers = copy.deepcopy(self.cs.layers)
        # running index
        y = 0.
        # if the cross section contains layers
        if not len(self.cs.layers) == 0:
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
        if len(layers) == 0:
            self.switch = -1
        else:
            # for the beginning minY=cross-section-height
            minY = self.h
            # go through all layers
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
        self.percentChange = True
        for layer in self.cs.layers:
            if layer.focus:
                layer.h, layer.p = self.h * value, value
                self.update_all_graph()
                self.cs.calculate_weight_price()
                self.cs.calculate_strength()
                self.update_cs_information()
                return

    '''
    the method update_height change the height of the cross section shape
    and update the layers
    '''

    def update_height(self, value):
        a, self.h = value / self.h, value
        for layer in self.cs.layers:
            layer.y, layer.h = layer.y * a, layer.h * a
            self.update_all_graph()
        self.graph.ymax = self.h
        self.graph.y_ticks_major = self.h / 5.
        self.update_cs_information()

    '''
    the method update_width change the width of the cross section shape
    and update the layers
    '''

    def update_width(self, value):
        self.w = value
        self.graph.x_ticks_major = self.w / 5.
        self.graph.xmax = self.w
        for layer in self.cs.layers:
            layer.w = value
        self.update_all_graph()
        self.update_cs_information()

