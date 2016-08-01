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


class AckRect(GridLayout):
    cs = ObjectProperty()
    ackLeft = ObjectProperty()
    ackRight = ObjectProperty()

    # Constructor
    def __init__(self, **kwargs):
        super(AckRect, self).__init__(**kwargs)
        self.cols = 1
        self.padding=[10,10,10,10]
    
    '''
    create the gui of the ackRect-object
    '''
    def create_gui(self):
        self.sliderStrain = Slider(min=1e-10, max=0.1, value=1e-5)
        self.contentLayout = GridLayout(cols=2)
        self.ackLeft, self.ackRight = AckLeftRect(), AckRightRect()
        self.ackRight.set_ack(self), self.ackLeft.set_ack(self)
        self.ackLeft.set_ack_right(self.ackRight)
        self.ackRight.set_ack_left(self.ackLeft)
        self.ackLeft.set_cross_section(self.cs)
        self.ackRight.set_cross_section(self.cs)
        self.contentLayout.add_widget(self.ackLeft)
        self.contentLayout.add_widget(self.ackRight)
        self.add_widget(self.contentLayout)
        sliderLayout = GridLayout(cols=3, row_force_default=True,
                                  row_default_height=dp(40), size_hint_y=None, 
                                  height=dp(40))
        self.lblStrain = OwnLabel(text='strain: ')
        self.btnClear = OwnButton(text='clear')
        self.btnClear.bind(on_press=self.clear)
        self.hlp=GridLayout(cols=2)
        self.hlp.add_widget(self.btnClear)
        self.hlp.add_widget(self.lblStrain)
        sliderLayout.add_widget(self.hlp)
        sliderLayout.add_widget(self.sliderStrain)
        self.add_widget(sliderLayout)
        self.sliderStrain.bind(value=self.update_strain)
        
    '''
    the method set_cross_section was developed to say the view, 
    which cross section should it use
    '''

    def set_cross_section(self, cs):
        self.cs = cs
        self.create_gui()

    '''
    update the left and the right side
    '''

    def update(self):
        self.sliderStrain.value = 0
        self.ackRight.update()
        self.ackLeft.update()

    '''
    set the maximum of the slider
    '''

    def set_maxStrain(self, value):
        self.sliderStrain.max = value

    '''
    set the label text to the current value of 
    the sliderStrain
    '''

    def update_strain(self, instance, value):
        self.lblStrain.text = 'strain: ' + str('%.2E' % Decimal(str(value)))
        self.ackRight.update_plots()
        self.ackLeft.set_focus_position(value)

    '''
    return the current strain
    '''

    def get_currentStrain(self):
        return self.sliderStrain.value

    '''
    return the maximum strain
    '''

    def get_maxStrain(self):
        return self.sliderStrain.max
    
    '''
    delete the plots which aren't the curPlot and the focusplot
    '''

    def clear(self, btn):
        while len(self.ackLeft.graph.plots) > 2:
            for plot in self.ackLeft.graph.plots:
                if not plot == self.ackLeft.curPlot and not plot == self.ackLeft.focus:
                    self.ackLeft.graph.remove_plot(plot)
            self.ackLeft.graph._clear_buffer()
    
