import pygame
import pygame_gui

def create_button(x_position, y_position, width, height, text, manager):
    return pygame_gui.elements.UIButton(
                pygame.Rect((x_position, y_position), (width, height)),
                text,
                manager)

def create_label(x_position, y_position, width, height, text, manager):
    return pygame_gui.elements.UILabel(
                pygame.Rect((x_position, y_position), (width, height)),
                text,
                manager)

def create_drop_down(options_list, starting_option, x_position, y_position, width, height, manager):
    return pygame_gui.elements.UIDropDownMenu(
                options_list,
                starting_option,
                pygame.Rect((x_position, y_position), (width, height)),
                manager)

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