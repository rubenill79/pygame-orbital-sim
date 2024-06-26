# Importación de bibliotecas necesarias
import os, sys
import time
import webbrowser
import pygame
import pygame_gui
import gui.component_builder as gui
import gui.matplotlib_controller as plt
import misc.sfx_player as sfx
import misc.image_loader as img
import misc.preset_loader as pst
from save_load import GeneralSettings, SimSettings, VideoSettings, AudioSettings
from sim.presets import CustomPreset
from gui.window_sim_controller import SimControllerWindow
from gui.window_plot_controller import PlotControllerWindow
from gui.window_plot import PlotWindow

# Definición de la clase principal del juego
class App:
    def __init__(self):
        # Inicialización de Pygame
        pygame.init()
        # Configuración del reloj principal
        self.clock = pygame.time.Clock()
        # Obtención de información sobre el monitor
        self.monitor_info = pygame.display.Info()
        # Resoluciones para pantalla completa y ventana
        self.resolution_fullscreen = (self.monitor_info.current_w, self.monitor_info.current_h)
        self.resolution_windowed_1600_800 = (1600, 800)
        self.resolution_windowed_1280_720 = (1280, 720)
        # Carga de la configuración de video guardada previamente
        self.fullscreen, self.current_resolution = VideoSettings.load_video_settings()
        if self.current_resolution == (0,0): self.current_resolution = self.resolution_fullscreen
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Configuración de la pantalla
        self.screen = self.set_screen()
        # Fuente y fondo
        self.font = pygame.font.Font('data/fonts/m5x7.otf', 24)
        self.background = img.load_img('menu_background')
        self.background = pygame.transform.scale(self.background, (self.current_resolution))
        # Opciones
        self.language, self.show_lenght_scale, self.show_FPS, self.show_advanced_data = GeneralSettings.load_general_settings()
        self.distance_mag, self.angle_mag, self.mass_mag, self.density_mag, self.planet_size, self.enable_mouse_hover = SimSettings.load_sim_settings()
        self.music_volume, self.gui_volume = AudioSettings.load_audio_settings()
        self.languages_list = ['pygame-gui.Spanish','pygame-gui.English']
        self.resolutions_list = ['pygame-gui.Native','1600x800','1280x720']
        self.graphics_list = ['pygame-gui.Attraction_forces','pygame-gui.None']
        self.presets_dictionary, self.presets_file_names = pst.load_presets('data/presets/')
        self.presets_list = pst.get_presets_name(self.presets_dictionary)
        self.descriptions_list = pst.get_presets_description(self.presets_dictionary)
        self.offline_mode = False
        # Sonido
        self.sfx_database = sfx.load_sfx('resources/sfx/')
        self.setup_gui_volume()
        pygame.mixer.music.load('resources/music/Arcadia.mp3')
        pygame.mixer.music.play(-1)
        self.setup_music_volume()
        # Simulacion actual
        self.simulation = None
        # Crear managers para cada gui
        self.main_menu_manager = self.create_ui_manager()
        self.selection_menu_manager = self.create_ui_manager()
        self.play_menu_manager = self.create_ui_manager()
        self.credits_menu_manager = self.create_ui_manager()
        self.options_menu_manager = self.create_ui_manager()
        self.general_options_menu_manager = self.create_ui_manager()
        self.simulation_options_menu_manager = self.create_ui_manager()
        self.video_options_menu_manager = self.create_ui_manager()
        self.audio_options_menu_manager = self.create_ui_manager()
        # Crear guis y aplicar idiomas guardados
        self.create_main_menu_gui()
        self.create_selection_menu_gui()
        self.create_credits_menu_gui()
        self.create_options_menu_gui()
        self.create_general_options_menu_gui()
        self.create_simulation_options_menu_gui()
        self.create_video_options_menu_gui()
        self.create_audio_options_menu_gui()
        self.set_locale(self.language)
        # Cosas adicionales
        pygame.display.set_icon(pygame.image.load('resources/icon/icon.ico'))
        pygame.display.set_caption('Simulador Orbital')
    # Métodos genéricos
    def go_back(self):
        sfx.play_sound('Menu_Sound_Backwards', self.sfx_database)
        return False
    def go_back_to_main_menu(self):
        sfx.play_sound('Menu_Sound_Backwards', self.sfx_database)
        self.simulation = None
        self.reset_ui_managers()
        return False
    def set_screen(self):   
        if self.fullscreen:
            return pygame.display.set_mode(self.current_resolution, pygame.FULLSCREEN, 32)
        elif self.current_resolution == self.resolution_fullscreen:
            return pygame.display.set_mode((int(self.current_resolution[0]),int(self.current_resolution[1]*0.96)), 0, 32, 0, 0)
        else:
             return pygame.display.set_mode(self.current_resolution, 0, 32, 0, 0)
    def setup_gui_volume(self):
        for sound in self.sfx_database:
            self.sfx_database[sound].set_volume(self.gui_volume)
    def setup_music_volume(self):
        pygame.mixer.music.set_volume(self.music_volume)
    def create_ui_manager(self):
        return pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()),
                                            theme_path='data/themes/main_theme.json',
                                            starting_language='es',
                                            translation_directory_paths=['data/translations'])
    def set_locale(self, language):
        self.language = language
        self.main_menu_manager.set_locale(self.language)
        self.selection_menu_manager.set_locale(self.language)
        self.play_menu_manager.set_locale(self.language)
        self.reset_localized_variables()
        self.credits_menu_manager.set_locale(self.language)
        self.options_menu_manager.set_locale(self.language)
        self.general_options_menu_manager.set_locale(self.language)
        self.simulation_options_menu_manager.set_locale(self.language)
        self.video_options_menu_manager.set_locale(self.language)
        self.audio_options_menu_manager.set_locale(self.language)
    def reset_ui_managers(self):
        self.main_menu_manager.clear_and_reset()
        self.main_menu_manager = self.create_ui_manager()
        self.create_main_menu_gui()
        self.selection_menu_manager.clear_and_reset()
        self.selection_menu_manager = self.create_ui_manager()
        self.create_selection_menu_gui()
        if self.simulation is not None:
            self.play_menu_manager.clear_and_reset()
            self.play_menu_manager = self.create_ui_manager()
            self.create_play_menu_gui()
            self.reset_localized_variables()
        self.credits_menu_manager.clear_and_reset()
        self.credits_menu_manager = self.create_ui_manager()
        self.create_credits_menu_gui()
        self.options_menu_manager.clear_and_reset()
        self.options_menu_manager = self.create_ui_manager()
        self.create_options_menu_gui()
        self.general_options_menu_manager.clear_and_reset()
        self.general_options_menu_manager = self.create_ui_manager()
        self.create_general_options_menu_gui()
        self.video_options_menu_manager.clear_and_reset()
        self.video_options_menu_manager = self.create_ui_manager()
        self.create_video_options_menu_gui()
        self.audio_options_menu_manager.clear_and_reset()
        self.audio_options_menu_manager = self.create_ui_manager()
        self.create_audio_options_menu_gui()
        self.simulation_options_menu_manager.clear_and_reset()
        self.simulation_options_menu_manager = self.create_ui_manager()
        self.create_simulation_options_menu_gui()
        self.set_locale(self.language)
    def change_manager(self, manager):
        sfx.play_sound('Menu_Sound_Forward', self.sfx_database)
        return manager
    def change_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.change_resolution()
    def change_resolution(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.current_resolution, pygame.FULLSCREEN, 32, 0, 0)
            pygame.mouse.set_pos(self.current_resolution[0] / 2, self.current_resolution[1] / 2)
            VideoSettings.save_video_settings(VideoSettings(self.fullscreen, self.current_resolution))
        elif self.current_resolution == self.resolution_fullscreen:
            self.screen = pygame.display.set_mode((int(self.current_resolution[0]),int(self.current_resolution[1]*0.96)), 0, 32, 0, 0)
            pygame.mouse.set_pos(self.current_resolution[0]*0.9 / 2, self.current_resolution[1]*0.9 / 2)
            VideoSettings.save_video_settings(VideoSettings(self.fullscreen, (0,0)))
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        else:
            self.screen = pygame.display.set_mode(self.current_resolution, 0, 32, 0, 0)
            pygame.mouse.set_pos(self.current_resolution[0] / 2, self.current_resolution[1] / 2)
            VideoSettings.save_video_settings(VideoSettings(self.fullscreen, self.current_resolution))
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.reset_ui_managers()
        if self.simulation is not None: self.simulation.check_resolution(self)
        self.background = pygame.transform.scale(self.background, (self.current_resolution))
    def change_music_volume(self, volume):
        self.music_volume = volume
        self.setup_music_volume()
        AudioSettings.save_audio_settings(AudioSettings(self.music_volume, self.gui_volume))
    def change_gui_volume(self, volume):
        self.gui_volume = volume
        self.setup_gui_volume()
        AudioSettings.save_audio_settings(AudioSettings(self.music_volume, self.gui_volume))
    def check_tf_button(self, variable):
        return '✓' if variable else 'X'
    def check_play_pause_button(self, variable):
        return '⏵' if variable else '⏸'
    def create_main_menu_gui(self):
        # Definición de los botones del menú
        self.main_menu_elements = [
                ("pygame-gui.Load_sim", self.screen.get_width()/2 - 200, self.screen.get_height()/2 - 120),
                ("pygame-gui.Options", self.screen.get_width()/2 - 200, self.screen.get_height()/2 - 60),
                ("pygame-gui.Guide", self.screen.get_width()/2 - 200, self.screen.get_height()/2),
                ("pygame-gui.Credits", self.screen.get_width()/2 - 200, self.screen.get_height()/2 + 60),
                ("pygame-gui.Desktop", self.screen.get_width()/2 - 200, self.screen.get_height()/2 + 120)
        ]
        self.main_menu_element = []
        # Create buttons and update their positions
        for element_text, x_position, y_position in self.main_menu_elements:
            self.main_menu_element.append(gui.create_button(x_position, y_position, 400, 50, element_text, self.main_menu_manager))
        self.main_menu_element[2].disable()
    def create_selection_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.selection_menu_elements = [
            ("pygame-gui.Select", self.screen.get_width()/2 - 600, self.screen.get_height()/10),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/10),
            ("", self.screen.get_width()/2 - 600, self.screen.get_height()/5),
            ("pygame-gui.Connection_mode", self.screen.get_width()/2 - 600, self.screen.get_height() - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height() - 200),
            ("pygame-gui.Launch_sim", self.screen.get_width()/2 - 375, self.screen.get_height() - 100),
            ("pygame-gui.Back", self.screen.get_width()/2 + 125, self.screen.get_height() - 100),
        ]
        self.selection_menu_elements_list = []
        # Create buttons and labels and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.selection_menu_elements):
            if i == 5 or i == 6: self.selection_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, element_text, self.selection_menu_manager))
            elif i == 0 or i == 3: self.selection_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), 50, element_text, self.selection_menu_manager))
            elif i == 1:
                try: 
                    self.selection_menu_elements_list.append(gui.create_drop_down(self.presets_list, self.presets_list[0], x_position, y_position, 400, 50, self.selection_menu_manager))
                    error = False
                except IndexError: 
                    self.selection_menu_elements_list.append(gui.create_drop_down(['pygame-gui.Error_presets'], 'pygame-gui.Error_presets', x_position, y_position, 400, 50, self.selection_menu_manager))
                    error = True
            elif i == 4: 
                self.selection_menu_elements_list.append(gui.create_button(x_position, y_position, 400, 50, self.check_tf_button(self.offline_mode), self.selection_menu_manager))
                if not error:
                    try: self.presets_dictionary[self.presets_file_names[0]]["online_entity_data"]
                    except KeyError:
                        self.offline_mode = not self.offline_mode
                        self.selection_menu_elements_list[4].set_text(self.check_tf_button(self.offline_mode))
                        self.selection_menu_elements_list[4].disable()
                    try: self.presets_dictionary[self.presets_file_names[0]]["offline_entity_data"]
                    except KeyError: self.selection_menu_elements_list[4].disable()
            else: 
                try: self.selection_menu_elements_list.append(gui.create_text_box(self.descriptions_list[0], x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), self.screen.get_height()/2, self.selection_menu_manager))
                except IndexError: self.selection_menu_elements_list.append(gui.create_text_box('pygame-gui.Error_presets', x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), self.screen.get_height()/2, self.selection_menu_manager))
    def create_credits_menu_gui(self):
        self.credits_menu_elements = [
            ("pygame-gui.Credits_html", self.screen.get_width()/2 - 500, self.screen.get_height()/8),
            ("pygame-gui.Back", self.screen.get_width()/2 - 500, self.screen.get_height() - 100)
        ]
        self.credits_menu_elements_list = []
        for i, (element_text, x_position, y_position) in enumerate(self.credits_menu_elements):
            if i == 0: self.credits_menu_elements_list.append(gui.create_text_box(element_text, x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 750), self.screen.get_height()/1.5, self.credits_menu_manager))
            elif i == 1: self.credits_menu_elements_list.append(gui.create_button(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 750), 50, element_text, self.credits_menu_manager))     
    def create_play_menu_gui(self):
        self.play_menu_elements = [
            ("≡", "pygame-gui.Menu_tooltip", self.screen.get_width() - 70, 20),
            ("?", "pygame-gui.Help_tooltip", self.screen.get_width() - 120, 20),
            ("⏮", "pygame-gui.Decrease_speed_tooltip", self.screen.get_width() / 2 - 125, 20),
            ("⏵", "pygame-gui.Pause_resume_tooltip", self.screen.get_width() / 2 - 25, 20),
            ("⏭", "pygame-gui.Increase_speed_tooltip", self.screen.get_width() / 2 + 25, 20),
            ("pygame-gui.Sim_controller_window", "", 20, 100),
            ("pygame-gui.Plot_controller_window", "", self.screen.get_width() - 5 - self.screen.get_width() / 4, 70),
            ("pygame-gui.Plot_window", "", self.screen.get_width() - 5 - self.screen.get_width() / 4, self.screen.get_height() / 2),
        ]
        """
        ("S", "pygame-gui.Sim_controller_tooltip", self.screen.get_width() - 170, 20),
        ("PC", "pygame-gui.Plot_controller_tooltip", self.screen.get_width() - 220, 20),
        ("G", "pygame-gui.Plot_tooltip", self.screen.get_width() - 270, 20)
        """
        self.play_menu_element = []
        for i, (element_text, tooltip, x_position, y_position) in enumerate(self.play_menu_elements):
            if i == 5: self.play_menu_element.append(SimControllerWindow((x_position, y_position), (self.screen.get_width() / 4, self.screen.get_height() / 2 + 15), self.play_menu_manager, element_text, self.simulation))
            elif i == 6: self.play_menu_element.append(PlotControllerWindow((x_position, y_position), (self.screen.get_width() / 4 - 17, self.screen.get_height() / 2 - 70), self.play_menu_manager, element_text, self.simulation))
            elif i == 7: self.play_menu_element.append(PlotWindow((x_position, y_position), (self.screen.get_width() / 4 - 17, self.screen.get_height() / 2), self.play_menu_manager, element_text, self.simulation))
            elif i == 0 or i == 1 or i == 3 or i == 8 or i == 9 or i == 10: self.play_menu_element.append(gui.create_button_with_id_and_tooltip_text(x_position, y_position, 50, 50, element_text, tooltip, self.play_menu_manager, '#menu_button'))
            else: self.play_menu_element.append(gui.create_button_with_id_and_tooltip_text(x_position, y_position, 100, 50, element_text, tooltip, self.play_menu_manager, '#menu_button'))
        self.play_menu_element[1].disable()
    def reset_localized_variables(self):
        self.play_text_elements = [
            ("Sim_paused"),
            ("Diameter"),
            ("Mass"),
            ("Density"),
            ("Position"),
            ("Eccentricity"),
            ("Major_axis"),
            ("Velocity"),
            ("Per_day"),
            ("Angle"),
            ("Simulating"),
            ("And"),
            ("Per_second"),
            ("Hours"),
            ("Minutes"),
            ("High_speed"),
            ("Sim_error"),
            ("Physics_update"),
            ("Small_diameter"),
            ("Orbital_period"),
            ("Earth_years"),
            ("Arg_periapsis"),
            ("Entity_count"),
            ("Physics_time"),
            ("Render_time"),
        ]
        for i, (element_text) in enumerate(self.play_text_elements):
            if i == 0: self.simulation_paused_text = pst.get_localized_text(element_text, self.language)
            elif i == 1: self.diameter_text = pst.get_localized_text(element_text, self.language)
            elif i == 2: self.mass_text = pst.get_localized_text(element_text, self.language)
            elif i == 3: self.density_text = pst.get_localized_text(element_text, self.language)
            elif i == 4: self.position_text = pst.get_localized_text(element_text, self.language)
            elif i == 5: self.eccentricity_text = pst.get_localized_text(element_text, self.language)
            elif i == 6: self.major_axis_text = pst.get_localized_text(element_text, self.language)
            elif i == 7: self.velocity_text = pst.get_localized_text(element_text, self.language)
            elif i == 8: self.per_day_text = pst.get_localized_text(element_text, self.language)
            elif i == 9: self.angle_text = pst.get_localized_text(element_text, self.language)
            elif i == 10: self.simulating_text = pst.get_localized_text(element_text, self.language)
            elif i == 11: self.and_text = pst.get_localized_text(element_text, self.language)
            elif i == 12: self.per_second_text = pst.get_localized_text(element_text, self.language)
            elif i == 13: self.hours_text = pst.get_localized_text(element_text, self.language)
            elif i == 14: self.minutes_text = pst.get_localized_text(element_text, self.language)
            elif i == 15: self.high_speed_text = pst.get_localized_text(element_text, self.language)
            elif i == 16: self.sim_error_text = pst.get_localized_text(element_text, self.language)
            elif i == 17: self.physics_update_text = pst.get_localized_text(element_text, self.language)
            elif i == 18: self.small_diameter_text = pst.get_localized_text(element_text, self.language)
            elif i == 19: self.orbital_period_text = pst.get_localized_text(element_text, self.language)
            elif i == 20: self.earth_years_text = pst.get_localized_text(element_text, self.language)
            elif i == 21: self.arg_periapsis_text = pst.get_localized_text(element_text, self.language)
            elif i == 22: self.entity_count_text = pst.get_localized_text(element_text, self.language)
            elif i == 23: self.physics_time_text = pst.get_localized_text(element_text, self.language)
            elif i == 24: self.render_time_text = pst.get_localized_text(element_text, self.language)
    def create_options_menu_gui(self):
        # Definición de los botones de opciones
        self.options_menu_elements = None
        self.options_menu_elements = []
        self.options_menu_elements = [
            ("pygame-gui.General", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 200),
            ("pygame-gui.Simulation", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 140),
            ("pygame-gui.Video", self.screen.get_width()/2 - 500, self.screen.get_height()/2- 80),
            ("pygame-gui.Audio", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 20),
        ]
        if self.simulation is not None:
            self.options_menu_elements.append(("pygame-gui.Back_simulation", self.screen.get_width()/2 - 500, self.screen.get_height() - 160))
            self.options_menu_elements.append(("pygame-gui.Exit_simulation", self.screen.get_width()/2 - 500, self.screen.get_height() - 100))
        else: self.options_menu_elements.append(("pygame-gui.Back", self.screen.get_width()/2 - 500, self.screen.get_height() - 100))
        self.options_menu_element = None
        self.options_menu_element = []
        # Create buttons and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.options_menu_elements):
            if i == 4 or i == 5: self.options_menu_element.append(gui.create_button(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 750), 50, element_text, self.options_menu_manager))    
            else: self.options_menu_element.append(gui.create_button(x_position, y_position, 200, 50, element_text, self.options_menu_manager))
    def create_general_options_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.general_options_menu_elements = [
            ("pygame-gui.Language", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("pygame-gui.Show_lenght_scale", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
            ("pygame-gui.FPS", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 80),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 80),
            ("pygame-gui.Advanced_data", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 20),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 20),
        ]
        self.general_options_menu_elements_list = []
        # Create buttons and labels and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.general_options_menu_elements):
            if i%2 == 0: self.general_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 300), 50, element_text, self.general_options_menu_manager))
            elif i == 1:
                if self.language == 'en': language = 'pygame-gui.English'
                elif self.language == 'es': language = 'pygame-gui.Spanish'
                # Create the dropdown menu
                self.general_options_menu_elements_list.append(gui.create_drop_down(self.languages_list, language, x_position, y_position, 250, 50, self.general_options_menu_manager))
            elif i == 3: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_lenght_scale), self.general_options_menu_manager))
            elif i == 5: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_FPS), self.general_options_menu_manager))
            elif i == 7: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_advanced_data), self.general_options_menu_manager))
            #else: self.general_options_menu_elements_list.append(gui.create_label(x_position, y_position, 250, 50, element_text, self.general_options_menu_manager))
    def create_simulation_options_menu_gui(self):
        self.simulation_options_menu_elements = [
            ("pygame-gui.M_distance", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("pygame-gui.M_angle", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
            ("pygame-gui.M_mass", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 80),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 80),
            ("pygame-gui.M_density", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 20),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 20),
            ("pygame-gui.Planet_size", self.screen.get_width()/2 - 300, self.screen.get_height()/2 + 40),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 + 40),
            ("pygame-gui.Mouse_hover", self.screen.get_width()/2 - 300, self.screen.get_height()/2 + 100),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 + 100),
        ]
        self.simulation_options_menu_elements_list = []
        # Create buttons and labels and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.simulation_options_menu_elements):
            if i%2 == 0: self.simulation_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 300), 50, element_text, self.simulation_options_menu_manager))
            elif i == 11: self.simulation_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.enable_mouse_hover), self.simulation_options_menu_manager))
            else: 
                self.simulation_options_menu_elements_list.append(gui.create_drop_down(['pygame-gui.Not_available'], 'pygame-gui.Not_available', x_position, y_position, 250, 50, self.simulation_options_menu_manager))
                self.simulation_options_menu_elements_list[i].disable()
    def create_video_options_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.video_options_menu_elements = [
            ("pygame-gui.Resolution", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("pygame-gui.Fullscreen", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
        ]
        self.video_options_menu_elements_list = []
        for i, (element_text, x_position, y_position) in enumerate(self.video_options_menu_elements):
            if i%2 == 0: self.video_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 300), 50, element_text, self.video_options_menu_manager))
            elif i == 3: self.video_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.fullscreen), self.video_options_menu_manager))
            elif i == 1:
                if self.current_resolution == self.resolution_fullscreen: resolution = 'pygame-gui.Native'
                elif self.current_resolution == self.resolution_windowed_1600_800: resolution = '1600x800'
                elif self.current_resolution == self.resolution_windowed_1280_720: resolution = '1280x720'
                # Create the dropdown menu
                self.video_options_menu_elements_list.append(gui.create_drop_down(self.resolutions_list, resolution, x_position, y_position, 250, 50, self.video_options_menu_manager))
    def create_audio_options_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.audio_options_menu_elements = [
            ("pygame-gui.Music_volume", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2, self.screen.get_height()/2 - 200),
            ("pygame-gui.Gui_volume", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2, self.screen.get_height()/2 - 140),
        ]
        self.audio_options_menu_elements_list = []
        for i, (element_text, x_position, y_position) in enumerate(self.audio_options_menu_elements):
            if i == 0 or i == 3: self.audio_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 300), 50, element_text, self.audio_options_menu_manager))
            elif i == 1 or i == 4:
                if i == 1: volume = self.music_volume * 100
                if i == 4: volume = self.gui_volume * 100
                self.audio_options_menu_elements_list.append(gui.create_horizontal_slider(x_position, y_position, 250, 50, volume, [0,100], self.audio_options_menu_manager))
            elif i == 2 or i == 5:
                if i == 2: volume = self.music_volume * 100
                if i == 5: volume = self.gui_volume * 100
                self.audio_options_menu_elements_list.append(gui.create_label(x_position, y_position, 200, 50, str(int(volume)), self.audio_options_menu_manager))
    def check_menu_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: return self.go_back()
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            sfx.play_sound('Menu_Sound_Hover', self.sfx_database)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return True
    # Métodos para prcesar cualquier input de la simulación
    def handle_simulation_command_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    def handle_simulation_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: self.simulation.left_click = True
            if event.button == 3: self.simulation.mouse_start_pos = pygame.mouse.get_pos()
            elif event.button == 4: self.simulation.zoom(1.0526)
            elif event.button == 5: self.simulation.zoom(0.95)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]: self.simulation.left_click = True
            if event.buttons[2]:
                self.simulation.left_click = False
                #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                mouse_current_pos = pygame.mouse.get_pos()
                mouse_offset_x = mouse_current_pos[0] - self.simulation.mouse_start_pos[0]
                mouse_offset_y = mouse_current_pos[1] - self.simulation.mouse_start_pos[1]
                self.simulation.scroll(dx=mouse_offset_x / 100, dy=mouse_offset_y / 100)
    def handle_simulation_key_events(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: self.pause()
            elif event.key == pygame.K_SPACE and not self.simulation.ended: 
                self.simulation.paused = not self.simulation.paused
                self.play_menu_element[3].set_text(self.check_play_pause_button(self.simulation.paused))
            elif event.key == pygame.K_q: self.simulation.zoom(1.0526)
            elif event.key == pygame.K_e: self.simulation.zoom(0.95)
            elif event.key == pygame.K_r: self.simulation.reset_zoom()
            elif event.key == pygame.K_PERIOD: self.simulation.change_sim_rate(1.2)
            elif event.key == pygame.K_COMMA: self.simulation.change_sim_rate(0.8)
            elif event.key == pygame.K_l: self.simulation.show_labels = not self.simulation.show_labels
        # Handling arrow key events for scrolling
        if keys[pygame.K_a]: self.simulation.scroll(dx=10)
        if keys[pygame.K_d]: self.simulation.scroll(dx=-10)
        if keys[pygame.K_w]: self.simulation.scroll(dy=10)
        if keys[pygame.K_s]: self.simulation.scroll(dy=-10)
    def handle_simulation_gui_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            self.simulation.left_click = False
            if event.ui_element == self.play_menu_element[0]: self.pause()
            if event.ui_element == self.play_menu_element[2]: self.simulation.change_sim_rate(0.8)
            if event.ui_element == self.play_menu_element[3] and not self.simulation.ended: 
                self.simulation.paused = not self.simulation.paused
                self.play_menu_element[3].set_text(self.check_play_pause_button(self.simulation.paused))
            if event.ui_element == self.play_menu_element[4]: self.simulation.change_sim_rate(1.2)
            # Mostrar entidades
            if event.ui_element == self.play_menu_element[5].entities_camera_center_button:
                self.simulation.show_camera_center = not self.simulation.show_camera_center
                self.play_menu_element[5].entities_camera_center_button.set_text(self.check_tf_button(self.simulation.show_camera_center))
            elif event.ui_element == self.play_menu_element[5].entities_focus_1_button:
                self.simulation.show_entities_focus_1 = not self.simulation.show_entities_focus_1
                self.play_menu_element[5].entities_focus_1_button.set_text(self.check_tf_button(self.simulation.show_entities_focus_1))
            elif event.ui_element == self.play_menu_element[5].entities_focus_2_button:
                self.simulation.show_entities_focus_2 = not self.simulation.show_entities_focus_2
                self.play_menu_element[5].entities_focus_2_button.set_text(self.check_tf_button(self.simulation.show_entities_focus_2))
            # Dibujar gráfico
            if event.ui_element == self.play_menu_element[6].matplotlib_draw_graphic:
                sfx.play_sound('Menu_Sound_Load_Savefile', self.sfx_database)
                for graphic in self.graphics_list:
                    if self.play_menu_element[6].matplotlib_type_choose_objects.selected_option[0] == graphic:
                        for entity in self.simulation.orbital_system.entities:
                            if self.play_menu_element[6].matplotlib_entities_choose_objects.selected_option[0] == entity.name:
                                self.play_menu_element[7].figuresurf = plt.draw(graphic, entity)
                                self.play_menu_element[7].update_figuresurf()
        elif event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            self.button_hovered = True
            sfx.play_sound('Menu_Sound_Hover', self.sfx_database)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            self.button_hovered = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    def handle_simulation_sub_windows_events(self, event):
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.play_menu_element[5].entities_camera_center_objects:
                self.simulation.focus = True
                self.simulation.focus_camera_index = self.play_menu_element[5].entities_camera_center_objects.options_list.index(self.play_menu_element[5].entities_camera_center_objects.selected_option)
            if event.ui_element == self.play_menu_element[5].entities_focus_1_objects:
                #self.simulation.overpass_mouse_hover = True
                self.simulation.focus_1_index = self.play_menu_element[5].entities_focus_1_objects.options_list.index(self.play_menu_element[5].entities_focus_1_objects.selected_option)
                self.simulation.focus_1_last_index = self.simulation.focus_1_index
                if self.play_menu_element[5].entities_focus_2_objects.selected_option != "pygame-gui.None": self.simulation.overpass_mouse_hover = True
            if event.ui_element == self.play_menu_element[5].entities_focus_2_objects:
                self.simulation.overpass_mouse_hover = True
                self.simulation.focus_2_index = self.play_menu_element[5].entities_focus_2_objects.options_list.index(self.play_menu_element[5].entities_focus_2_objects.selected_option)
                self.simulation.focus_2_last_index = self.simulation.focus_2_index
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            if event.ui_element == self.play_menu_element[5].title_bar or event.ui_element == self.play_menu_element[6].title_bar or event.ui_element == self.play_menu_element[7].title_bar:
                self.sub_window = True
                self.sub_window_button_hovered = True
        if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            if event.ui_element == self.play_menu_element[5].title_bar or event.ui_element == self.play_menu_element[6].title_bar or event.ui_element == self.play_menu_element[7].title_bar:
                self.sub_window = False
                self.sub_window_button_hovered = False
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.play_menu_element[5].title_bar or event.ui_element == self.play_menu_element[6].title_bar or event.ui_element == self.play_menu_element[7].title_bar:
                self.sub_window = True
                self.sub_window_button_hovered = True
        self.handle_simulation_gui_events(event)
        self.play_menu_manager.process_events(event)
    def handle_simulation_sub_windows_mouse_pos(self):
        if self.play_menu_element[5].get_relative_mouse_pos() is not None: 
            if self.sub_window_button_hovered: self.sub_window_button_hovered = False
            else: self.sub_window = True
        elif self.play_menu_element[6].get_relative_mouse_pos() is not None: 
            if self.sub_window_button_hovered: self.sub_window_button_hovered = False
            else: self.sub_window = True
        elif self.play_menu_element[7].get_relative_mouse_pos() is not None: 
            if self.sub_window_button_hovered: self.sub_window_button_hovered = False
            else: self.sub_window = True
        else:
            if self.sub_window_button_hovered is True: pass
            else: self.sub_window = False
    # Método para dibujar y actualizar culaquier escena
    def update_and_draw_gui(self, delta_time, managers):
        for manager in managers:
            manager.update(delta_time)
        if self.simulation is None:
            self.screen.fill((0,0,0))
            self.screen.blit(self.background,(0,0))
        else: self.simulation.draw(self, self.clock)
        version_display = self.font.render("V 1.0.5", 1, (255,255,255))
        self.screen.blit(version_display, (20, self.screen.get_height() - 40 ))
        for manager in managers:
            manager.draw_ui(self.screen)
        pygame.display.update()
    # Método del menú principal del juego
    def main_menu(self):
        while True:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    sfx.play_sound('Menu_Sound_Forward', self.sfx_database)
                    if event.ui_element == self.main_menu_element[0]: self.select()
                    elif event.ui_element == self.main_menu_element[1]: self.options()
                    elif event.ui_element == self.main_menu_element[2]: pass#self.guide() 
                    elif event.ui_element == self.main_menu_element[3]: self.credits()
                    elif event.ui_element == self.main_menu_element[4]:
                        pygame.quit()
                        sys.exit()

                self.main_menu_manager.process_events(event)
            self.update_and_draw_gui(delta_time, [self.main_menu_manager])
    # Método para la selección de sistema
    def select(self):
        running = True 
        while running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.check_menu_events(event)
                running = self.check_menu_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.selection_menu_elements_list[6]: running = self.go_back()
                    elif event.ui_element == self.selection_menu_elements_list[4]:
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.offline_mode = not self.offline_mode
                        self.selection_menu_elements_list[4].set_text(self.check_tf_button(self.offline_mode))
                    elif event.ui_element == self.selection_menu_elements_list[5]:
                        sfx.play_sound('Menu_Sound_Load_Savefile', self.sfx_database)
                        for i, preset_name in enumerate(self.presets_list):
                            if self.selection_menu_elements_list[1].selected_option[0] == preset_name:
                                self.simulation_(i)
                                running = False
                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED: webbrowser.open_new_tab(event.link_target)
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('Menu_Sound_Load_Savefile', self.sfx_database)
                    for i, preset_name in enumerate(self.presets_list):
                        if event.text == preset_name:
                            self.selection_menu_elements_list[2].set_text(self.descriptions_list[i])
                            # Sistema de detección de modos json
                            self.selection_menu_elements_list[4].enable()
                            self.selection_menu_elements_list[5].enable()                          
                            try:
                                self.presets_dictionary[self.presets_file_names[i]]["offline_entity_data"]
                                offline = True
                            except KeyError: offline = False
                            try:
                                self.presets_dictionary[self.presets_file_names[i]]["online_entity_data"]
                                online = True
                            except KeyError: online = False
                            if offline and online:
                                self.offline_mode = not offline
                                self.selection_menu_elements_list[4].set_text(self.check_tf_button(self.offline_mode))
                            elif (offline and not online) or (not offline and online):
                                self.offline_mode = offline
                                self.selection_menu_elements_list[4].set_text(self.check_tf_button(self.offline_mode))
                                self.selection_menu_elements_list[4].rebuild()
                                self.selection_menu_elements_list[4].disable()
                            else:
                                self.selection_menu_elements_list[4].set_text(self.check_tf_button(False))
                                self.selection_menu_elements_list[4].rebuild()
                                self.selection_menu_elements_list[4].disable()
                                self.selection_menu_elements_list[5].disable()                   
                                    
                if not running: return
                self.selection_menu_manager.process_events(event)
            self.update_and_draw_gui(delta_time, [self.selection_menu_manager])
    # Método para la pantalla de la simulación    
    def simulation_(self, index):
        self.simulation = CustomPreset(self, prest_json=self.presets_dictionary[self.presets_file_names[index]])
        self.simulation.start()
        self.button_hovered = False
        self.sub_window = False
        self.sub_window_button_hovered = False
        self.reset_ui_managers()
        self.paused = False
        running = True 
        while running:
            delta_time = self.clock.tick(500)
            # manejador de eventos
            # Encapsular en funcion de comprobador de hover de ventanas
            for event in pygame.event.get(eventtype=[pygame_gui.UI_DROP_DOWN_MENU_CHANGED, pygame_gui.UI_BUTTON_ON_HOVERED, pygame_gui.UI_BUTTON_ON_UNHOVERED, pygame_gui.UI_BUTTON_START_PRESS]):
                self.handle_simulation_sub_windows_events(event)
                self.play_menu_manager.process_events(event)
            self.handle_simulation_sub_windows_mouse_pos()
            for event in pygame.event.get(exclude=[pygame_gui.UI_BUTTON_PRESSED]):
                self.handle_simulation_command_events(event)
                if not self.sub_window: self.handle_simulation_mouse_events(event)
                self.handle_simulation_key_events(event)
                self.handle_simulation_gui_events(event)
                self.play_menu_manager.process_events(event)
            for event in pygame.event.get(eventtype=[pygame_gui.UI_BUTTON_PRESSED]):
                self.handle_simulation_gui_events(event)
                if self.simulation is None: return
                self.play_menu_manager.process_events(event)

            # actualizacion de físicas
            if not self.simulation.paused:
                self.simulation.physics_delta_t += delta_time
                # actualizar 50 veces por segundo
                if self.simulation.physics_delta_t >= 20:
                    self.simulation.update(self, self.simulation.physics_delta_t)
                    self.simulation.physics_delta_t = 0
            # Dibujar simulación
            self.update_and_draw_gui(delta_time, [self.play_menu_manager])
    # Método para la pausa
    def pause(self):
        sfx.play_sound('Menu_Sound_Backwards', self.sfx_database)
        self.paused = True
        self.options()
        self.paused = False       
    # Método para la pantalla de opciones
    def options(self):
        running = True
        current_manager = self.general_options_menu_manager
        while running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                running = self.check_menu_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.options_menu_element[0]: current_manager = self.change_manager(self.general_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[1]: current_manager = self.change_manager(self.simulation_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[2]: current_manager = self.change_manager(self.video_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[3]: current_manager = self.change_manager(self.audio_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[4]: running = self.go_back()
                    try: 
                        if event.ui_element == self.options_menu_element[5]: running = self.go_back_to_main_menu()
                    except IndexError: pass
                    if event.ui_element == self.general_options_menu_elements_list[3]: 
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.show_lenght_scale = not self.show_lenght_scale
                        self.general_options_menu_elements_list[3].set_text(self.check_tf_button(self.show_lenght_scale))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.show_lenght_scale, self.show_FPS, self.show_advanced_data))
                    if event.ui_element == self.general_options_menu_elements_list[5]: 
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.show_FPS = not self.show_FPS
                        self.general_options_menu_elements_list[5].set_text(self.check_tf_button(self.show_FPS))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.show_lenght_scale, self.show_FPS, self.show_advanced_data))
                    elif event.ui_element == self.general_options_menu_elements_list[7]:
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.show_advanced_data = not self.show_advanced_data
                        self.general_options_menu_elements_list[7].set_text(self.check_tf_button(self.show_advanced_data))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.show_lenght_scale, self.show_FPS, self.show_advanced_data))
                    elif event.ui_element == self.video_options_menu_elements_list[3]:
                        self.change_fullscreen()
                        self.video_options_menu_elements_list[3].set_text(self.check_tf_button(self.fullscreen))
                        current_manager = self.video_options_menu_manager
                    elif event.ui_element == self.simulation_options_menu_elements_list[11]:
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.enable_mouse_hover = not self.enable_mouse_hover
                        self.simulation_options_menu_elements_list[11].set_text(self.check_tf_button(self.enable_mouse_hover))
                        SimSettings.save_sim_settings(SimSettings(self.distance_mag, self.angle_mag, self.mass_mag, self.density_mag, self.planet_size, self.enable_mouse_hover))
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('Menu_Sound_Load_Savefile', self.sfx_database)
                    if event.ui_element == self.general_options_menu_elements_list[1]:
                        if event.text == 'pygame-gui.English': self.set_locale('en')
                        elif event.text == 'pygame-gui.Spanish': self.set_locale('es')
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.show_lenght_scale, self.show_FPS, self.show_advanced_data))
                    if event.ui_element == self.video_options_menu_elements_list[1]:
                        if event.text == 'pygame-gui.Native': self.current_resolution = self.resolution_fullscreen
                        elif event.text == '1600x800': self.current_resolution = self.resolution_windowed_1600_800
                        elif event.text == '1280x720': self.current_resolution = self.resolution_windowed_1280_720
                        self.change_resolution()
                        current_manager = self.video_options_menu_manager
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.audio_options_menu_elements_list[1]:
                        self.change_music_volume(round(event.value/100, 2))
                        self.audio_options_menu_elements_list[2].set_text(str(int(self.music_volume*100)))
                    if event.ui_element == self.audio_options_menu_elements_list[4]:
                        self.change_gui_volume(round(event.value/100, 2))
                        self.audio_options_menu_elements_list[5].set_text(str(int(self.gui_volume*100)))
                if not running: return
                current_manager.process_events(event)
                self.options_menu_manager.process_events(event) 
            self.update_and_draw_gui(delta_time, [self.options_menu_manager, current_manager])
    # Método para la pantalla de créditos
    def credits(self):
        running = True 
        while running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.check_menu_events(event)
                running = self.check_menu_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.credits_menu_elements_list[1]: running = self.go_back()
                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED: webbrowser.open_new_tab(event.link_target)
                if not running: return
                self.credits_menu_manager.process_events(event)
            self.update_and_draw_gui(delta_time, [self.credits_menu_manager])