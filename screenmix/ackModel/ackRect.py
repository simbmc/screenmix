'''
Created on 15.04.2016
@author: mkennert
'''
from decimal import Decimal

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider

from ackModel.ackLeftRect import AckLeftRect
from ackModel.ackRightRect import AckRightRect
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel
from ownComponents.design import Design


class AckRect(GridLayout):
    '''
    ackrect is the ack-component of the rectangle-shape
    '''
    cs = ObjectProperty()
    ackLeft = ObjectProperty()
    ackRight = ObjectProperty()

    # Constructor
    def __init__(self, **kwargs):
        super(AckRect, self).__init__(**kwargs)
        self.cols = 1
    
    '''
    create the gui of the ackRect-object
    '''
    def create_gui(self):
        self.sliderStrain = Slider(min=1e-10, max=0.1, value=1e-5)
        self.create_ack_components()
        self.contentLayout = GridLayout(cols=2)
        self.contentLayout.add_widget(self.ackLeft)
        self.contentLayout.add_widget(self.ackRight)
        self.add_widget(self.contentLayout)
        sliderLayout = GridLayout(cols=3, row_force_default=True,
                                  row_default_height=dp(40), size_hint_y=None,
                                  height=dp(40))
        self.lblStrain = OwnLabel(text='strain: ')
        self.btnClear = OwnButton(text='clear')
        self.btnClear.bind(on_press=self.clear)
        self.hlp = GridLayout(cols=2)
        self.hlp.add_widget(self.btnClear)
        self.hlp.add_widget(self.lblStrain)
        sliderLayout.add_widget(self.hlp)
        sliderLayout.add_widget(self.sliderStrain)
        self.add_widget(sliderLayout)
        self.sliderStrain.bind(value=self.update_strain)
    
    '''
    create all ackRect-components
    '''
    def create_ack_components(self):
        self.ackLeft, self.ackRight = AckLeftRect(), AckRightRect()
        self.ackRight.ack = self
        self.ackLeft.ack = self
        self.ackLeft.ackRight = self.ackRight
        self.ackRight.ackLeft = self.ackLeft
        self.ackLeft.cs = self.cs
        self.ackRight.cs = self.cs
        self.ackRight.create_graph()
        self.ackRight.update()
    
    '''
    update the left and the right side
    '''

    def update(self):
        self.sliderStrain.value = 0
        self.ackRight.update()
        self.ackLeft.update()


    '''
    set the label text to the current value of 
    the sliderStrain
    '''

    def update_strain(self, instance, value):
        self.lblStrain.text = 'strain: ' + str('%.2E' % Decimal(str(value)))
        self.ackRight.update_plots()
        self.ackLeft.move_position(value)

    
    '''
    delete the plots which aren't the curPlot and the focusplot
    '''

    def clear(self, btn):
        while len(self.ackLeft.graph.plots) > 2:
            for plot in self.ackLeft.graph.plots:
                if not plot == self.ackLeft.curPlot and not plot == self.ackLeft.focus:
                    self.ackLeft.graph.remove_plot(plot)
            self.ackLeft.graph._clear_buffer()
