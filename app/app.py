# Importación de bibliotecas necesarias
import os, sys
import pygame
import pygame_gui
import gui_components as gui
import webbrowser
from save_load import GeneralSettings, VideoSettings, AudioSettings
import sfx_player as sfx
import image_loader as img
import preset_loader as pst
from game.presets import CustomPreset

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
        # Fondo
        self.background = img.load_img('menu_background')
        self.background = pygame.transform.scale(self.background, (self.current_resolution))
        # Opciones
        self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS = GeneralSettings.load_general_settings()
        self.music_volume, self.gui_volume = AudioSettings.load_audio_settings()
        self.languages_list = ['pygame-gui.Spanish','pygame-gui.English']
        self.resolutions_list = ['pygame-gui.Native','1600x800','1280x720']
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
        self.options_menu_manager = self.create_ui_manager()
        self.general_options_menu_manager = self.create_ui_manager()
        self.video_options_menu_manager = self.create_ui_manager()
        self.audio_options_menu_manager = self.create_ui_manager()
        # Crear guis y aplicar idiomas guardados
        self.create_main_menu_gui()
        self.create_selection_menu_gui()
        self.create_play_menu_gui()
        self.create_options_menu_gui()
        self.create_general_options_menu_gui()
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
        self.options_menu_manager.set_locale(self.language)
        self.general_options_menu_manager.set_locale(self.language)
        self.video_options_menu_manager.set_locale(self.language)
        self.audio_options_menu_manager.set_locale(self.language)
        if self.simulation is not None:
            self.play_menu_manager.clear_and_reset()
            self.play_menu_manager = self.create_ui_manager()
            self.create_play_menu_gui()
    def reset_ui_managers(self):
        self.main_menu_manager.clear_and_reset()
        self.main_menu_manager = self.create_ui_manager()
        self.create_main_menu_gui()
        self.selection_menu_manager.clear_and_reset()
        self.selection_menu_manager = self.create_ui_manager()
        self.create_selection_menu_gui()
        self.play_menu_manager.clear_and_reset()
        self.play_menu_manager = self.create_ui_manager()
        self.create_play_menu_gui()
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
        if variable == True: return '✓'
        else: return 'X'
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
                try: self.selection_menu_elements_list.append(gui.create_drop_down(self.presets_list, self.presets_list[0], x_position, y_position, 400, 50, self.selection_menu_manager))
                except IndexError: self.selection_menu_elements_list.append(gui.create_drop_down(['pygame-gui.Error_presets'], 'pygame-gui.Error_presets', x_position, y_position, 400, 50, self.selection_menu_manager))
            elif i == 4: self.selection_menu_elements_list.append(gui.create_button(x_position, y_position, 400, 50, self.check_tf_button(self.offline_mode), self.selection_menu_manager))
            else: 
                try: self.selection_menu_elements_list.append(gui.create_text_box(self.descriptions_list[0], x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), self.screen.get_height()/2, self.selection_menu_manager))
                except IndexError: self.selection_menu_elements_list.append(gui.create_text_box('pygame-gui.Error_presets', x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), self.screen.get_height()/2, self.selection_menu_manager))
    def create_play_menu_gui(self):
        self.play_menu_elements = [
            ("≡", self.screen.get_width() - 70, 20),
            ("Sim_paused", 0, 0),
            ("Diameter", 0, 0),
            ("Mass", 0, 0),
            ("Density", 0, 0),
            ("Position", 0, 0),
            ("Eccentricity", 0, 0),
            ("Major_axis", 0, 0),
            ("Velocity", 0, 0),
            ("Day", 0, 0),
            ("Angle", 0, 0),
            ("Simulating", 0, 0),
            ("And", 0, 0),
            ("Per_second", 0, 0),
            ("Hours", 0, 0),
            ("Minutes", 0, 0),
            ("High_speed", 0, 0),
            ("Sim_error", 0, 0),
            ("Physics_update", 0, 0),
        ]
        self.play_menu_element = []
        for i, (element_text, x_position, y_position) in enumerate(self.play_menu_elements):
            if i == 0:
                self.play_menu_element.append(gui.create_button_with_id(x_position, y_position, 50, 50, element_text, self.play_menu_manager, '#menu_button'))
            elif i == 1: self.simulation_paused_text = pst.get_localized_text(element_text, self.language)
            elif i == 2: self.diameter_text = pst.get_localized_text(element_text, self.language)
            elif i == 3: self.mass_text = pst.get_localized_text(element_text, self.language)
            elif i == 4: self.density_text = pst.get_localized_text(element_text, self.language)
            elif i == 5: self.position_text = pst.get_localized_text(element_text, self.language)
            elif i == 6: self.eccentricity_text = pst.get_localized_text(element_text, self.language)
            elif i == 7: self.major_axis_text = pst.get_localized_text(element_text, self.language)
            elif i == 8: self.velocity_text = pst.get_localized_text(element_text, self.language)
            elif i == 9: self.day_text = pst.get_localized_text(element_text, self.language)
            elif i == 10: self.angle_text = pst.get_localized_text(element_text, self.language)
            elif i == 11: self.simulating_text = pst.get_localized_text(element_text, self.language)
            elif i == 12: self.and_text = pst.get_localized_text(element_text, self.language)
            elif i == 13: self.per_second_text = pst.get_localized_text(element_text, self.language)
            elif i == 14: self.hours_text = pst.get_localized_text(element_text, self.language)
            elif i == 15: self.minutes_text = pst.get_localized_text(element_text, self.language)
            elif i == 16: self.high_speed_text = pst.get_localized_text(element_text, self.language)
            elif i == 17: self.sim_error_text = pst.get_localized_text(element_text, self.language)
            elif i == 18: self.physics_update_text = pst.get_localized_text(element_text, self.language)
    def create_options_menu_gui(self):
        # Definición de los botones de opciones
        self.options_menu_elements = None
        self.options_menu_elements = []
        self.options_menu_elements = [
            ("pygame-gui.General", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 200),
            ("pygame-gui.Simulation", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 140),
            ("pygame-gui.Video", self.screen.get_width()/2 - 500, self.screen.get_height()/2- 80),
            ("pygame-gui.Audio", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 20),
            ("pygame-gui.Controls", self.screen.get_width()/2 - 500, self.screen.get_height()/2 + 40),
        ]
        if self.simulation is not None:
            self.options_menu_elements.append(("pygame-gui.Back_simulation", self.screen.get_width()/2 - 500, self.screen.get_height() - 160))
            self.options_menu_elements.append(("pygame-gui.Exit_simulation", self.screen.get_width()/2 - 500, self.screen.get_height() - 100))
        else: self.options_menu_elements.append(("pygame-gui.Back", self.screen.get_width()/2 - 500, self.screen.get_height() - 100))
        self.options_menu_element = None
        self.options_menu_element = []
        # Create buttons and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.options_menu_elements):
            if i == 5 or i == 6: self.options_menu_element.append(gui.create_button(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 750), 50, element_text, self.options_menu_manager))    
            else: self.options_menu_element.append(gui.create_button(x_position, y_position, 200, 50, element_text, self.options_menu_manager))
    def create_general_options_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.general_options_menu_elements = [
            ("pygame-gui.Language", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("pygame-gui.Gui_scale", self.screen.get_width()/2 - 300, self.screen.get_height()/2 - 140),
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
            elif i == 5: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_FPS), self.general_options_menu_manager))
            elif i == 7: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_advanced_data), self.general_options_menu_manager))
            else: self.general_options_menu_elements_list.append(gui.create_label(x_position, y_position, 250, 50, element_text, self.general_options_menu_manager))
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
    def check_play_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            sfx.play_sound('Menu_Sound_Hover', self.sfx_database)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        return True
    def update_and_draw_gui(self, delta_time, managers):
        for manager in managers:
            manager.update(delta_time)
        if self.simulation is None:
            self.screen.fill((0,0,0))
            self.screen.blit(self.background,(0,0))
        else: self.simulation.draw(self, self.clock)
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
                    elif event.ui_element == self.main_menu_element[3]: pass#self.credits()
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
                            if self.selection_menu_elements_list[1].selected_option == preset_name:
                                self.simulation_(i)
                                running = False

                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED: webbrowser.open_new_tab(event.link_target)
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('Menu_Sound_Load_Savefile', self.sfx_database)
                    for i, preset_name in enumerate(self.presets_list):
                        if event.text == preset_name:
                            self.selection_menu_elements_list[2].set_text(self.descriptions_list[i])   
                            
                if not running: return
                self.selection_menu_manager.process_events(event)
            self.update_and_draw_gui(delta_time, [self.selection_menu_manager])
    # Método para la pantalla de la simulación    
    def simulation_(self, index):
        self.simulation = CustomPreset(self, prest_json=self.presets_dictionary[self.presets_file_names[index]])
        self.simulation.start(self)
        self.reset_ui_managers()
        self.paused = False
        running = True 
        while running:
            delta_time = self.clock.tick(500)
            # manejador de eventos
            for event in pygame.event.get():
                self.check_play_events(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sfx.play_sound('Menu_Sound_Backwards', self.sfx_database)
                        self.paused = True
                        self.options()
                        self.paused = False
                        if self.simulation is None: return
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_menu_element[0]:
                        sfx.play_sound('Menu_Sound_Backwards', self.sfx_database)
                        self.paused = True
                        self.options()
                        self.paused = False
                        if self.simulation is None: return     
                self.simulation.handle_event(event)
                self.play_menu_manager.process_events(event)
            # actualizacion de físicas
            if not self.simulation.paused:
                self.simulation.physics_delta_t += delta_time
                # actualizar 50 veces por segundo
                if self.simulation.physics_delta_t >= 20:
                    self.simulation.update(self.simulation.physics_delta_t)
                    self.simulation.physics_delta_t = 0
            # Dibujar simulación
            self.update_and_draw_gui(delta_time, [self.play_menu_manager])
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
                    elif event.ui_element == self.options_menu_element[1]: pass#current_manager = self.change_manager(self.simulation_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[2]: current_manager = self.change_manager(self.video_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[3]: current_manager = self.change_manager(self.audio_options_menu_manager)
                    elif event.ui_element == self.options_menu_element[4]: pass#current_manager = self.change_manager(self.controls_menu_manager)
                    elif event.ui_element == self.options_menu_element[5]: running = self.go_back()
                    try: 
                        if event.ui_element == self.options_menu_element[6]: running = self.go_back_to_main_menu()
                    except IndexError: pass
                    if event.ui_element == self.general_options_menu_elements_list[5]: 
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.show_FPS = not self.show_FPS
                        self.general_options_menu_elements_list[5].set_text(self.check_tf_button(self.show_FPS))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS))
                    elif event.ui_element == self.general_options_menu_elements_list[7]:
                        sfx.play_sound('Menu_Sound_Save_Savefile', self.sfx_database)
                        self.show_advanced_data = not self.show_advanced_data
                        self.general_options_menu_elements_list[7].set_text(self.check_tf_button(self.show_advanced_data))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS))
                    elif event.ui_element == self.video_options_menu_elements_list[3]:
                        self.change_fullscreen()
                        self.video_options_menu_elements_list[3].set_text(self.check_tf_button(self.fullscreen))
                        current_manager = self.video_options_menu_manager
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('Menu_Sound_Load_Savefile', self.sfx_database)
                    if event.ui_element == self.general_options_menu_elements_list[1]:
                        if event.text == 'pygame-gui.English': self.set_locale('en')
                        elif event.text == 'pygame-gui.Spanish': self.set_locale('es')
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS))
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