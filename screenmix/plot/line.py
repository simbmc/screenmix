from math import log10

from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.graphics import Line
from kivy.garden.graph import Plot, Color

class LinePlot(Plot):
    '''LinePlot draws using a standard Line object.
    '''
    
    '''Args:
    line_width (float) - the width of the graph line
    '''
    def __init__(self, **kwargs):
        self._line_width = kwargs.get('line_width', 3)
        super(LinePlot, self).__init__(**kwargs)
    
    def create_drawings(self):
        from kivy.graphics import Line, RenderContext

        self._grc = RenderContext(
                use_parent_modelview=True,
                use_parent_projection=True)
        with self._grc:
            self._gcolor = Color(*self.color)
            self._gline = Line(points=[], cap='none', width=self._line_width, joint='round')

        return [self._grc]
    
    def draw(self, *args):
        super(LinePlot, self).draw(*args)
        # flatten the list
        points = []
        for x, y in self.iterate_points():
            points += [x, y]
        self._gline.points = points

if __name__ == '__main__':
    from kivy.uix.boxlayout import BoxLayout
    from kivy.app import App
    from kivy.garden.graph import Graph
    import random
    from kivy.clock import Clock

    class TestApp(App):

        def build(self):
            b = BoxLayout(orientation='vertical')

            graph2 = Graph(
                xlabel='x',
                ylabel='y',
                x_ticks_major=10,
                y_ticks_major=10,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                xmin=0,
                ymin=0)

            plot = LinePlot()
            plot.points=[(0,0),(10,10)]
            graph2.add_plot(plot)

            b.add_widget(graph2)
            self.circle = plot

            #Clock.schedule_interval(self.update_color, 1)
            #Clock.schedule_interval(self.update_pos, 1)

            return b

        def update_color(self, *args):
            self.circle.color = [random.randint(0, 255) for r in xrange(100)]
