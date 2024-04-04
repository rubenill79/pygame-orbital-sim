import pygame
import pygame_gui

from pygame_gui.elements.ui_window import UIWindow

class SimControllerWindow(UIWindow):
    def __init__(self, position: tuple, size: tuple, ui_manager, title, simulation):
        super().__init__(pygame.Rect(position, size), ui_manager,
                         window_display_title=title,
                         object_id='#sim_controller_window')
        

        
        #game_surface_size = self.get_container().get_size()
        """
        self.game_surface_element = UIImage(pygame.Rect((0, 0),
                                                        game_surface_size),
                                            pygame.Surface(game_surface_size).convert(),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)
        """
        self.entities_list = []
        for i, entity in enumerate(simulation.orbital_system.entities):
            self.entities_list.append(entity.name)
        self.entities_list.append("pygame-gui.None")
        self.top_left_offsett = 20
        self.space_between_same_ui_elements = self.rect.width / 12
        self.space_between_distinct_ui_elements = self.rect.width / 4
            
        self.entities_camera_center_label = pygame_gui.elements.UILabel(pygame.Rect((20,self.top_left_offsett/2),(self.rect.width - 70, 50)),
                                                  "pygame-gui.Camera_center",
                                                  self.ui_manager,
                                                  container=self)
        self.entities_camera_center_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  "pygame-gui.None",
                                                  pygame.Rect((20,self.space_between_same_ui_elements + self.top_left_offsett),(self.rect.width - 70, 50)),
                                                  self.ui_manager,
                                                  container=self)
        self.entities_focus_1_label = pygame_gui.elements.UILabel(pygame.Rect((20,self.space_between_distinct_ui_elements + self.top_left_offsett / 2),(self.rect.width - 70, 50)),
                                                  "pygame-gui.Focus_1",
                                                  self.ui_manager,
                                                  container=self)
        self.entities_focus_1_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  "pygame-gui.None",
                                                  pygame.Rect((20,self.space_between_distinct_ui_elements + self.space_between_same_ui_elements + self.top_left_offsett),(self.rect.width - 70, 50)),
                                                  self.ui_manager,
                                                  container=self)
        self.entities_focus_2_label = pygame_gui.elements.UILabel(pygame.Rect((20,self.space_between_distinct_ui_elements*2 + self.top_left_offsett / 2),(self.rect.width - 70, 50)),
                                                  "pygame-gui.Focus_2",
                                                  self.ui_manager,
                                                  container=self)
        self.entities_focus_2_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  "pygame-gui.None",
                                                  pygame.Rect((20,self.space_between_distinct_ui_elements*2 + self.space_between_same_ui_elements + self.top_left_offsett),(self.rect.width - 70, 50)),
                                                  self.ui_manager,
                                                  container=self)

        #self.pong_game = PongGame(game_surface_size)

        #self.is_active = False
    """
    def process_event(self, event):
        
        handled = super().process_event(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == "#entities_window.#title_bar" and
                event.ui_element == self.title_bar):
            handled = True
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            window_selected_event = pygame.event.Event(LIST_WINDOW_SELECTED,
                                                       event_data)
            pygame.event.post(window_selected_event)
        
        return handled
"""
    # Overrride method to stop the window from closing
    def on_close_window_button_pressed(self):
        pass

    def update(self, time_delta):
        #if self.alive() and self.is_active:
            #self.pong_game.update(time_delta)

        super().update(time_delta)

        #self.pong_game.draw(self.game_surface_element.image)
        
    def update_externaly_changed_entities_camera_center_objects(self, option):
        self.entities_camera_center_objects.kill()
        self.entities_camera_center_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  option,
                                                  pygame.Rect((20,self.space_between_same_ui_elements + self.top_left_offsett),(self.rect.width - 70, 50)),
                                                  self.ui_manager,
                                                  container=self)
    
    def update_externaly_changed_entities_focus_1_objects(self, option):
        self.entities_focus_1_objects.kill()
        self.entities_focus_1_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  option,
                                                  pygame.Rect((20,self.space_between_distinct_ui_elements + self.space_between_same_ui_elements + self.top_left_offsett),(self.rect.width - 70, 50)),
                                                  self.ui_manager,
                                                  container=self)
        
    def update_externaly_changed_entities_focus_2_objects(self, option):
        self.entities_focus_2_objects.kill()
        self.entities_focus_2_objects = pygame_gui.elements.UIDropDownMenu(self.entities_list,
                                                  option,
                                                  pygame.Rect((20,self.space_between_distinct_ui_elements*2 + self.space_between_same_ui_elements + self.top_left_offsett),(self.rect.width - 70, 50)),
                                                  self.ui_manager,
                                                  container=self)