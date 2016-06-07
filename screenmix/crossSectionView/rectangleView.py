'''
Created on 14.03.2016
@author: mkennert
'''


from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from itertools import cycle
from crossSectionView.layerRectangle import LayerRectangle
from plot.filled_rect import FilledRect
from designClass.design import Design
colors = [[255, 102, 102], [255, 255, 102], [140, 255, 102], [102, 255, 217],
          [102, 102, 255], [255, 102, 102], [179, 179, 179], [102, 71, 133]]
colorcycler = cycle(colors)


'''
the class CSRectangleView was developed to show the the cross section,
which has a rectangle shape
'''


class CSRectangleView(BoxLayout):
    # Constructor

    def __init__(self, **kwargs):
        super(CSRectangleView, self).__init__(**kwargs)
        self.h = 0.5
        self.w = 0.25
        self.percentChange = False
        self.layers = []
        self.create_graph()
    
    '''
    update the layers in the graph
    '''
    def update_all_graph(self):
        for layer in self.layers:
            y = layer.y
            h = layer.h
            layer.filledRectCs.xrange =[0., self.w]
            layer.filledRectCs.yrange=[y - h / 2., y + h / 2.]
            if layer.focus:
                layer.filledRectCs.color = Design.focusColor
            else:
                layer.filledRectCs.color=layer.colors
        if len(self.layers) == 0:
            self.graph._clear_buffer()
            
    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.w, ymin=0, ymax=self.h)
        self.add_widget(self.graph)

    '''
    the method on_touch_move is invoked after the user touch within a rectangle and move it.
    it changes the position of the rectangle
    '''

    def on_touch_move(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        gw, gh = self.graph._plot_area.size  # graph size
        x = (touch.x - x0) / gw * self.w
        y = (touch.y - y0) / gh * self.h
        for layer in self.layers:
            if layer.focus and layer.mouse_within_just_x_coordinate(x):
                # case:1 the layer don't collide with the border of the cross
                # section
                if y > layer.h / 2 and y < self.h - layer.h / 2:
                    layer.set_yrange([
                        y - layer.h / 2., y + layer.h / 2.])
                    layer.set_y(y)
                    return
                # case:2 the layer collide with the bottom border of the cross section
                #       the user can't move the layer down
                elif y < layer.h / 2:
                    layer.set_yrange([0., layer.h])
                    layer.set_y(layer.h / 2)
                    return
                # case:3 the layer collide with the top border of the cross section
                #       the user can't move the layer up
                elif y > self.h - layer.h / 2:
                    layer.set_yrange([
                        self.h - layer.h, self.h])
                    layer.set_y(
                        self.h - layer.h / 2)
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
        for layer in self.layers:
            if layer.mouse_within(x, y):
                if layer.focus == True and self.percentChange:
                    self.percentChange = False
                    self.update_all_graph()
                    return
                if layer.focus == False and curFocus == False:
                    layer.focus = True
                    curFocus = True
                    cur = layer.get_material_informations()
                    self.cs.set_layer_information(cur[0], cur[1], cur[
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
        cur = LayerRectangle(self.w / 2, self.h - h / 2., h,
                              self.w, next(colorcycler), value)
        cur.set_material(material)
        y = cur.y
        h = cur.h
        filledRectCs = FilledRect(xrange=[0., self.w],
                                    yrange=[y - h / 2., y + h / 2.],
                                    color=cur.colors)
        filledRectAck=FilledRect(xrange=[0.,0.],
                                 yrange=[y - h / 2., y + h / 2.],
                                 color=cur.colors)
        self.graph.add_plot(filledRectCs)
        cur.set_filledrect_cs(filledRectCs)
        cur.set_filledrect_Ack(filledRectAck)
        self.layers.append(cur)
        self.update_all_graph()
        self.cs.calculate_strength()
        self.update_cross_section_information()

    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        for layer in self.layers:
            if layer.focus:
                layer.filledRectCs.yrange=[0,0]
                layer.filledRectAck.yrange=[0,0]
                self.layers.remove(layer)
        self.update_all_graph()
        self.cs.calculate_strength()
        self.update_cross_section_information()

    '''
    the method update_layer_information update the layer information of 
    the view_information
    '''

    def update_layer_information(self, name, price, density, stiffness, strength, percent):
        self.cs.set_layer_information(
            name, price, density, stiffness, strength, percent)

    '''
    the method update_cross_section_information update the cross section information of 
    the view_information
    '''

    def update_cross_section_information(self):
        self.cs.calculate_weight_price()
        self.cs.set_cross_section_information()

    '''
    the method get_free_places return the free-places, 
    where is no layer
    '''

    def get_free_places(self):
        self.free_places = []
        # running index
        y = 0
        # if the cross section contains layers
        if not len(self.layers) == 0:
            while y < self.h:
                # layerExist is a switch to proofs whether
                # a layer exist over the runnning index or not
                layerExist = False
                minValue = self.h
                for layer in self.layers:
                    if layer.y >= y and layer.y < minValue:
                        layerExist = True
                        minValue = layer.y - layer.h / 2.
                        nextMinValue = layer.y + layer.h / 2.
                        # if the running index is equals the min, means that there's no
                        # area
                        if not y == minValue:
                            self.free_places.append((y, minValue))
                        y = nextMinValue
                # if no layer exist over the running index then that's the last
                # area which is free.
                if not layerExist:
                    self.free_places.append((y, self.h))
                    return self.free_places
        # if no layer exist,all area of the cross section is free
        else:
            self.free_places.append((0, self.h))
        return self.free_places

    ##########################################################################
    #                                Setter && Getter                        #
    ##########################################################################
    '''
    the method set_percent change the percent shape of the selected rectangle
    '''

    def set_percent(self, value):
        self.percentChange = True
        for rectangle in self.layers:
            if rectangle.focus:
                rectangle.set_height(self.h * value)
                rectangle.set_percent(value)
                self.update_all_graph()
                self.cs.calculate_strength()
                self.update_cross_section_information()
                return

    '''
    the method set_height change the height of the cross section shape
    and update the layers
    '''

    def set_height(self, value):
        for layer in self.layers:
            layer.set_y(
                layer.y / self.h * value)
            layer.set_height(
                layer.h / self.h * value)
            self.update_all_graph()
        self.h = value
        self.graph.ymax = self.h
        self.graph.y_ticks_major=self.h/5.
        self.update_cross_section_information()

    '''
    the method set_width change the width of the cross section shape
    and update the layers
    '''

    def set_width(self, value):
        self.w = value
        self.graph.x_ticks_major=self.w/5.
        self.graph.xmax = self.w
        for layer in self.layers:
            layer.set_width(value)
        self.update_all_graph()
        self.update_cross_section_information()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs

    '''
    return all layers 
    '''

    def get_layers(self):
        return self.layers