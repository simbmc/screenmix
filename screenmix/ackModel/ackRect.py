'''
Created on 15.04.2016
@author: mkennert
'''
from decimal import Decimal

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider

from ackModel.ackLeftRect import AckLeftRect
from ackModel.ackRightRect import AckRightRect
from ownComponents.design import Design
from ownComponents.ownButton import OwnButton
from ownComponents.ownLabel import OwnLabel


class AckRect(GridLayout):
    
    '''
    ackrect is the ack-component of the rectangle-shape. it's shows
    the stress of the each layers and the matrix of 
    the cross section
    '''
    
    # cross-section-shape
    cs = ObjectProperty()
    
    # left-component of the ack-rectangle
    ackLeft = ObjectProperty(AckLeftRect())
    
    # right-component of the ack-rectangle
    ackRight = ObjectProperty(AckRightRect())
    
    strainStr = StringProperty('strain: ')
    
    stressStr = StringProperty('stress: ')
    
    clearStr = StringProperty('clear')
    
    # constructor
    def __init__(self, **kwargs):
        super(AckRect, self).__init__(**kwargs)
        self.cols = 1
    
    '''
    create the gui of the ackRect-object. the gui contains the ack-left/right,
    the clear-btn and the slider.
    '''
        
    def create_gui(self):
        # slider to change the strain of the diagram
        self.sliderStrain = Slider(min=1e-10, max=0.1, value=1e-5)
        self.sliderStrain.bind(value=self.update_strain)
        # clear-btn to delete the plots, whichs has no focus
        self.btnClear = OwnButton(text=self.clearStr)
        self.btnClear.bind(on_press=self.clear)
        self.create_ack_components()  # create the necessary ack-components
        self.contentLayout = GridLayout(cols=2)  # create the layout for the ack-left/right
        self.contentLayout.add_widget(self.ackLeft)
        self.contentLayout.add_widget(self.ackRight)
        # create the area, for the clear-btn and the strainSlider
        # sliderlayout was used to make sure, that the 
        # height of the area is small
        sliderLayout = GridLayout(cols=2, row_force_default=True,
                                  row_default_height=Design.btnHeight, size_hint_y=None,
                                  height=1.1 * Design.btnHeight)
        # lbl to show the cur-strain
        self.lblStrain = OwnLabel(text=self.strainStr)
        self.lblStress = OwnLabel(text=self.stressStr)
        # hlp is used to to save space for the slider
        self.hlp = GridLayout(cols=3, padding=Design.padding)
        self.hlp.add_widget(self.btnClear)
        self.hlp.add_widget(self.lblStrain)
        self.hlp.add_widget(self.lblStress)
        sliderLayout.add_widget(self.hlp)
        sliderLayout.add_widget(self.sliderStrain)
        self.add_widget(self.contentLayout)
        self.add_widget(sliderLayout)

    
    '''
    create all ackRect-components
    '''
        
    def create_ack_components(self):
        self.ackRight.ack = self  # sign in by the ack
        self.ackLeft.ack = self
        # left/right sign in by the component to make 
        # a easier communication between the components 
        self.ackLeft.ackRight = self.ackRight
        self.ackRight.ackLeft = self.ackLeft 
        self.ackLeft.cs = self.cs 
        self.ackRight.cs = self.cs
        self.ackRight.create_graph()
        self.ackRight.update()
    
    '''
    delete the plots which aren't the curPlot and the focusplot. 
    this method was developed in order to avoid that the graph has 
    to much plots. so the user can always on time delete the plots
    '''
        
    def clear(self, btn):
        # while there is a plot, which is not the focus-point
        # or the cur-plot
        while len(self.ackLeft.graph.plots) > 2:
            # go through all plots
            for plot in self.ackLeft.graph.plots:
                # if the plot is not the focus-point or the cur-plot
                # delete the plot
                if not plot == self.ackLeft.curPlot and not plot == self.ackLeft.focus:
                    self.ackLeft.graph.remove_plot(plot)
            # clear the graph
            self.ackLeft.graph._clear_buffer()
        self.ackLeft.update_graph_border()
            
    '''
    update the left and the right side. by the update the strain will
    be set to the value 0.
    '''

    def update(self):
        self.sliderStrain.value = 0
        # update the graphs of the ack components
        self.ackRight.update()
        self.ackLeft.update()

    '''
    set the label-text to the current value of 
    the sliderStrain. so the user can see the the current 
    strain of the diagram
    '''

    def update_strain(self, instance, value):
        # make a sci-notation. it's necessary to avoid that the 
        # value is too long
        self.lblStrain.text = self.strainStr + str('%.2E' % Decimal(str(value)))
        
        # update the ackRight/Left after with new value
        self.ackRight.update_plots()
        self.ackLeft.move_position(value)
