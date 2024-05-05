import pygame
import pygame_gui
import gui.component_builder as gui

import pygame_gui.elements.ui_button
from pygame_gui.elements.ui_window import UIWindow

class PlotControllerWindow(UIWindow):
    def __init__(self, position: tuple, size: tuple, ui_manager, title, simulation):
        super().__init__(pygame.Rect(position, size), ui_manager,
                         window_display_title=title,
                         object_id='#plot_controller_window')
        
        
        self.entities_list = []
        self.graphics_list = [("pygame-gui.Attraction_forces"),("pygame-gui.None")]
        for i, entity in enumerate(simulation.orbital_system.entities):
            self.entities_list.append(entity.name)
        self.entities_list.append("pygame-gui.None")
        self.top_left_offsett = 20
        self.space_between_same_ui_elements = self.rect.width / 12
        self.space_between_distinct_ui_elements = self.rect.width / 4
            
        self.matplotlib_entities_choose_label = pygame_gui.elements.UILabel(pygame.Rect((0,0),(self.rect.width, 50)),
                                                  "pygame-gui.Plot_entity",
                                                  self.ui_manager,
                                                  container=self)
        self.matplotlib_entities_choose_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  "pygame-gui.None",
                                                  pygame.Rect((0,self.space_between_same_ui_elements + self.top_left_offsett + 1),(self.rect.width - 32, 50)),
                                                  self.ui_manager,
                                                  container=self)
        self.matplotlib_type_choose_label = pygame_gui.elements.UILabel(pygame.Rect((0,self.space_between_distinct_ui_elements + self.top_left_offsett / 2 + 3),(self.rect.width, 50)),
                                                  "pygame-gui.Plot_type",
                                                  self.ui_manager,
                                                  container=self)
        self.matplotlib_type_choose_objects = gui.create_drop_down_with_container_and_with_id(self.graphics_list,
                                                  "pygame-gui.None",
                                                  pygame.Rect((0,self.space_between_distinct_ui_elements + self.space_between_same_ui_elements + self.top_left_offsett + 14),(self.rect.width - 32, 50)),
                                                  self.ui_manager,
                                                  container=self,
                                                  object_id='#last_drop_down_menu')
        self.matplotlib_draw_graphic =  gui.create_button_with_container_and_tooltip_text(
                                        pygame.Rect((0,self.space_between_distinct_ui_elements*2 + self.top_left_offsett / 2 + 35),(self.rect.width - 32, 50)),
                                        "pygame-gui.Draw_plot",
                                        self.ui_manager,
                                        container=self,
                                        tool_tip_text="pygame-gui.Draw_plot_tooltip")
        
    # Overrride method to stop the window from closing
    def on_close_window_button_pressed(self):
        pass

    def update(self, time_delta):
        #if self.alive() and self.is_active:
            #self.pong_game.update(time_delta)

        super().update(time_delta)
        #self.pong_game.draw(self.game_surface_element.image)