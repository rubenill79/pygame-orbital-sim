import pygame
import pygame_gui
from pygame_gui.core import ObjectID

def create_button(x_position, y_position, width, height, text, manager):
    return pygame_gui.elements.UIButton(
                pygame.Rect((x_position, y_position), (width, height)),
                text,
                manager)

def create_button_with_id(x_position, y_position, width, height, text, manager, object_id):
    return pygame_gui.elements.UIButton(
                pygame.Rect((x_position, y_position), (width, height)),
                text,
                manager,
                object_id = ObjectID(object_id=object_id))

def create_button_with_id_and_tooltip_text(x_position, y_position, width, height, text, tool_tip_text, manager, object_id):
    button = pygame_gui.elements.UIButton(
                pygame.Rect((x_position, y_position), (width, height)),
                text,
                manager,
                object_id = ObjectID(object_id=object_id))
    button.set_tooltip(tool_tip_text, wrap_width=-1)
    return button

def create_button_with_container_and_tooltip_text(rect, text, manager, container, tool_tip_text):
    button = pygame_gui.elements.UIButton(
                pygame.Rect(rect),
                text,
                manager,
                container=container)
    button.set_tooltip(tool_tip_text, wrap_width=-1)
    return button

def create_label(x_position, y_position, width, height, text, manager):
    return pygame_gui.elements.UILabel(
                pygame.Rect((x_position, y_position), (width, height)),
                text,
                manager)
# def create_label_with_container(rect: pygame.Rect, text, manager, container): => pygame_gui.elements.UILabel
def create_label_with_container(rect, text, manager, container): 
    return pygame_gui.elements.UILabel(
                pygame.Rect(rect),
                text,
                manager,
                container=container)

def create_drop_down(options_list, starting_option, x_position, y_position, width, height, manager):
    return pygame_gui.elements.UIDropDownMenu(
                options_list,
                starting_option,
                pygame.Rect((x_position, y_position), (width, height)),
                manager)
# def create_drop_down_with_container_and_with_id(options_list, starting_option, rect: pygame.Rect, text, manager, container, object_id): => pygame_gui.elements.UIDropDownMenu
def create_drop_down_with_container_and_with_id(options_list, starting_option, rect, manager, container, object_id):
    return pygame_gui.elements.UIDropDownMenu(
                options_list,
                starting_option,
                pygame.Rect(rect),
                manager,
                container=container,
                object_id = ObjectID(object_id=object_id))

def create_text_box(html_text, x_position, y_position, width, height, manager):
    return pygame_gui.elements.UITextBox(
                html_text,
                pygame.Rect((x_position, y_position), (width, height)),
                manager)

def create_horizontal_slider(x_position, y_position, width, height, start_value, value_range, manager):
    return pygame_gui.elements.UIHorizontalSlider(
                pygame.Rect((x_position, y_position), (width, height)),
                start_value,
                value_range,
                manager)