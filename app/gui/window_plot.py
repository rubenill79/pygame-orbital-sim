import pygame
from .matplotlib_controller import *

import pygame_gui

from pygame_matplotlib.gui_window import UIPlotWindow

class PlotWindow(UIPlotWindow):
    def __init__(self, position: tuple, size: tuple, ui_manager, title, simulation):
        super().__init__(pygame.Rect(position, size), ui_manager,
                         figuresurface=fig,
                         window_display_title=title,
                         object_id='#plot_controller_window')
    
    # Overrride method to stop the window from closing
    def on_close_window_button_pressed(self):
        pass

    def update(self, time_delta):
        #if self.alive() and self.is_active:
            #self.pong_game.update(time_delta)

        super().update(time_delta)