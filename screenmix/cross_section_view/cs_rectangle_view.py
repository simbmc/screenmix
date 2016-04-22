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
colors = [[255, 102, 102], [255, 255, 102], [140, 255, 102], [102, 255, 217],
          [102, 102, 255], [255, 102, 102], [179, 179, 179], [102, 71, 133]]
colorcycler = cycle(colors)


'''
the class CS_Rectangle_View was developed to show the the cross section,
which has a rectangle shape
'''


class CS_Rectangle_View(BoxLayout, AView):
    # Constructor

    def __init__(self, **kwargs):
        super(CS_Rectangle_View, self).__init__(**kwargs)
        self.cross_section_height = 0.5
        self.cross_section_width = 0.25
        self.cross_section = None
        self.percent_change = False
        self.layers = []
        self.create_graph()
#         self.add_widget(self.update_all_graph)

    '''
    the method update_all_graph update the graph. the method should be called, when
    something has changed
    '''

    def update_all_graph(self):
        list = []
        for plot in self.graph.plots:
            list.append(plot)
        for layer in self.layers:
            y = layer.y_coordinate
            h = layer._height
            layer.rect = FilledRect(xrange=[0., self.cross_section_width],
                                    yrange=[y - h / 2., y + h / 2.],
                                    color=layer.colors)
            if layer.focus:
                layer.rect.color = [255, 255, 255]
            self.graph.add_plot(layer.rect)
        #delete the old plots
        for plot in list:
            self.graph.remove_plot(plot)
            self.graph._clear_buffer()
        if len(list) == 0:
            self.graph._clear_buffer()

    '''
    the method create_graph create the graph, where you can add 
    the layers. the method should be called only once at the beginning
    '''

    def create_graph(self):
        self.graph = Graph(
            x_ticks_major=0.05, y_ticks_major=0.05,
            y_grid_label=True, x_grid_label=True, padding=5,
            xmin=0, xmax=self.cross_section_width, ymin=0, ymax=self.cross_section_height)
        self.add_widget(self.graph)

    '''
    the method draw_layer was developed to get the points of the rectangle
    the while_loop was create to make the rectangle set a grid.
    '''
    @staticmethod
    def draw_layer(x_coordinate, y_coordinate, width, height):
        points = [(x_coordinate - width / 2., y_coordinate - height / 2.), (x_coordinate + width / 2., y_coordinate - height / 2.), (x_coordinate + width /
                                                                                                                                     2., y_coordinate + height / 2.), (x_coordinate - width / 2., y_coordinate + height / 2.), (x_coordinate - width / 2., y_coordinate - height / 2.)]
        i = 0
        delta = 1000.
        distance = width / delta
        while i < delta:
            points.append(
                (x_coordinate - width / 2. + distance, y_coordinate - height / 2.))
            points.append(
                (x_coordinate - width / 2. + distance, y_coordinate - height / 2. + height))
            distance += width / delta
            points.append(
                (x_coordinate - width / 2. + distance, y_coordinate - height / 2. + height))
            points.append(
                (x_coordinate - width / 2. + distance, y_coordinate - height / 2. + height))
            i += 1
        return points

    '''
    the method on_touch_move is invoked after the user touch within a rectangle and move it.
    it changes the position of the rectangle
    '''

    def on_touch_move(self, touch):
        x_coordinate = (touch.x / self.graph.width) / \
            (1 / self.cross_section_width)
        y_coordinate = (touch.y / self.graph.height) / \
            (1. / self.cross_section_height)
        for layer in self.layers:
            if layer.focus and layer.mouse_within_just_x_coordinate(x_coordinate):
                # case:1 the layer don't collide with the border of the cross
                # section
                if y_coordinate > layer._height / 2 and y_coordinate < self.cross_section_height - layer._height / 2:
                    layer.rect.yrange = [
                        y_coordinate - layer._height / 2., y_coordinate + layer._height / 2.]
                    layer.set_y_coordinate(y_coordinate)
                    return
                # case:2 the layer collide with the bottom border of the cross section
                #       the user can't move the layer down
                elif y_coordinate < layer._height / 2:
                    layer.rect.yrange = [0., layer._height]
                    layer.set_y_coordinate(layer._height / 2)
                    return
                # case:3 the layer collide with the top border of the cross section
                #       the user can't move the layer up
                elif y_coordinate > self.cross_section_height - layer._height / 2:
                    layer.rect.yrange = [
                        self.cross_section_height - layer._height, self.cross_section_height]
                    layer.set_y_coordinate(
                        self.cross_section_height - layer._height / 2)
                    return

    '''
    the method on_touch_down is invoked when the user touch within a rectangle.
    the rectangle get the focus and if a rectangle exist, which has the focus
    that lose it.
    '''

    def on_touch_down(self, touch):
        x0, y0 = self.graph._plot_area.pos  # position of the lowerleft
        graph_w, graph_h = self.graph._plot_area.size  # graph size
        x_coordinate = (touch.x - x0) / graph_w * self.cross_section_width
        y_coordinate = (touch.y - y0) / graph_h * self.cross_section_height
        changed = False
        one_is_already_focus = False
        for rectangle in self.layers:
            if rectangle.mouse_within(x_coordinate, y_coordinate):
                if rectangle.focus == True and self.percent_change:
                    self.percent_change = False
                    self.update_all_graph()
                    return
                if rectangle.focus == False and one_is_already_focus == False:
                    rectangle.focus = True
                    one_is_already_focus = True
                    cur_info = rectangle.get_material_informations()
                    self.cross_section.set_layer_information(cur_info[0], cur_info[1], cur_info[
                                                             2], cur_info[3], cur_info[4], rectangle._height / self.cross_section_height)
                    changed = True
            else:
                if rectangle.focus == True:
                    rectangle.focus = False
                    changed = True
        # update just when something has change
        if changed:
            self.update_all_graph()

    # not yet so relevant. maybe we have time, we can finished it
    '''
    def collide(self,x,y,_width,_height):
        for rectangle in self.layers:
            if not rectangle.equals(x, y, _width, _height):
                #Case:1
                if y+_height/2>rectangle.y_coordinate-rectangle._height/2 and y+_height/2<rectangle.y_coordinate-rectangle._height/2:
                    print('Fall:1')
                    return rectangle._height+_height
                #Case:2
                elif y-_height/2<rectangle.y_coordinate+rectangle._height/2 and y+_height/2>rectangle.y_coordinate+rectangle._height/2:
                    print('Fall:2')
                    return -rectangle._height-_height
        return 0
    '''

    '''
    the method add_layer was developed to add new layer at the cross section
    '''

    def add_layer(self, value, material):
        height = self.cross_section_height * value
        cur = Layer_Rectangle(self.cross_section_width / 2, self.cross_section_height - height / 2., height,
                              self.cross_section_width, next(colorcycler), value)
        cur.set_material(material)
        self.layers.append(cur)
        self.update_all_graph()
        self.cross_section.calculate_strength()
        self.update_cross_section_information()

    '''
    the method delete_layer was developed to delete layer from the cross section
    '''

    def delete_layer(self):
        for rectangle in self.layers:
            if rectangle.focus:
                self.layers.remove(rectangle)
        self.update_all_graph()
        self.cross_section.calculate_strength()
        self.update_cross_section_information()

    '''
    the method update_layer_information update the layer information of 
    the view_information
    '''

    def update_layer_information(self, name, price, density, stiffness, strength, percent):
        self.cross_section.set_layer_information(
            name, price, density, stiffness, strength, percent)

    '''
    the method update_cross_section_information update the cross section information of 
    the view_information
    '''

    def update_cross_section_information(self):
        self.cross_section.calculate_weight_price()
        self.cross_section.set_cross_section_information()

    '''
    the method get_free_places return the free-places, 
    where is no layer
    '''

    def get_free_places(self):
        self.free_places = []
        # running index
        cur_y = 0
        # if the cross section contains layers
        if not len(self.layers) == 0:
            while cur_y < self.cross_section_height:
                # layer_exist is a switch to proofs whether
                # a layer exist over the runnning index or not
                layer_exist = False
                min_value = self.cross_section_height
                for layer in self.layers:
                    if layer.y_coordinate >= cur_y and layer.y_coordinate < min_value:
                        layer_exist = True
                        min_value = layer.y_coordinate - layer._height / 2.
                        nextMinValue = layer.y_coordinate + layer._height / 2.
                        # if the running index is equals the min, means that there's no
                        # area
                        if not cur_y == min_value:
                            self.free_places.append((cur_y, min))
                        cur_y = nextMinValue
                # if no layer exist over the running index then that's the last
                # area which is free.
                if not layer_exist:
                    self.free_places.append((cur_y, self.cross_section_height))
                    return self.free_places
        # if no layer exist,all area of the cross section is free
        else:
            self.free_places.append((0, self.cross_section_height))
        return self.free_places

    ##########################################################################
    #                                Setter && Getter                                               #
    ##########################################################################
    '''
    the method set_percent change the percent shape of the selected rectangle
    '''

    def set_percent(self, value):
        self.percent_change = True
        for rectangle in self.layers:
            if rectangle.focus:
                rectangle.set_height(self.cross_section_height * value)
                rectangle.set_percentage(value)
                self.update_all_graph()
                self.cross_section.calculate_strength()
                self.update_cross_section_information()
                return

    '''
    the method set_height change the height of the cross section shape
    and update the layers
    '''

    def set_height(self, value):
        for rectangle in self.layers:
            rectangle.set_y_coordinate(
                rectangle.y_coordinate / self.cross_section_height * value)
            rectangle.set_height(
                rectangle._height / self.cross_section_height * value)
        self.cross_section_height = value
        self.graph.ymax = self.cross_section_height
        self.update_all_graph()
        self.update_cross_section_information()

    '''
    the method set_width change the width of the cross section shape
    and update the layers
    '''

    def set_width(self, value):
        self.cross_section_width = value
        self.graph.xmax = self.cross_section_width
        for rectangle in self.layers:
            rectangle.set_width(value)
        self.update_all_graph()
        self.update_cross_section_information()

    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cross_section):
        self.cross_section = cross_section

    '''
    return all layers 
    '''

    def get_layers(self):
        return self.layers
