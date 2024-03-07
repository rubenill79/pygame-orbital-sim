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
        #self.presets_list = ['Tierra - Luna','Sistema Solar Interno','Sistema Solar Completo','Sistema Solar Avanzado']
        self.offline_mode = False
        # Sonido
        self.sfx_database = sfx.load_sfx('resources/sfx/')
        self.setup_gui_volume()
        pygame.mixer.music.load('resources/music/Arcadia.mp3')
        pygame.mixer.music.play(-1)
        self.setup_music_volume()
        # Crear managers para cada gui
        self.main_menu_manager = self.create_ui_manager()
        self.selection_menu_manager = self.create_ui_manager()
        self.options_menu_manager = self.create_ui_manager()
        self.general_options_menu_manager = self.create_ui_manager()
        self.video_options_menu_manager = self.create_ui_manager()
        self.audio_options_menu_manager = self.create_ui_manager()
        # Crear guis y aplicar idiomas guardados
        self.create_main_menu_gui()
        self.create_selection_menu_gui()
        self.create_options_menu_gui()
        self.create_general_options_menu_gui()
        self.create_video_options_menu_gui()
        self.create_audio_options_menu_gui()
        self.set_locale(self.language)
        # Cosas adicionales
        pygame.display.set_icon(pygame.image.load('resources/icon/icon.ico'))
        pygame.display.set_caption('Simulador Orbital')
    # Método para configurar la pantalla
    def set_screen(self):   
        if self.fullscreen:
            return pygame.display.set_mode(self.current_resolution, pygame.FULLSCREEN, 32)
        elif self.current_resolution == self.resolution_fullscreen:
            return pygame.display.set_mode((int(self.current_resolution[0]),int(self.current_resolution[1]*0.96)), 0, 32, 0, 0)
        else:
             return pygame.display.set_mode(self.current_resolution, 0, 32, 0, 0)
    def setup_gui_volume(self):
        for sound in ['menu_change', 'menu_move', 'menu_select']:
            self.sfx_database[sound].set_volume(self.gui_volume if sound == 'menu_change' or sound == 'menu_select' else self.gui_volume*0.5)
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
    def reset_ui_managers(self):
        self.main_menu_manager.clear_and_reset()
        self.main_menu_manager = self.create_ui_manager()
        self.create_main_menu_gui()
        self.selection_menu_manager.clear_and_reset()
        self.selection_menu_manager = self.create_ui_manager()
        self.create_selection_menu_gui()
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
        self.main_menu_buttons = [
                ("pygame-gui.Play", 0, self.screen.get_height() - 100),
                ("pygame-gui.Options", 0, self.screen.get_height() - 100),
                ("pygame-gui.Credits", 0, self.screen.get_height() - 100),
                ("pygame-gui.Desktop", 0, self.screen.get_height() - 100)
        ]
        self.main_menu_button = []
        # Calculate the space between buttons
        self.space_between_main_menu_buttons = self.screen.get_width() / (len(self.main_menu_buttons) + 1)
        # Create buttons and update their positions
        for i, (button_text, _, y_position) in enumerate(self.main_menu_buttons):
            x_position = (i + 1) * self.space_between_main_menu_buttons - 110
            self.main_menu_button.append(gui.create_button(x_position, y_position, 220, 50, button_text, self.main_menu_manager))
    def create_selection_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.select_menu_elements = [
            ("pygame-gui.Select", self.screen.get_width()/2 - 600, self.screen.get_height()/10),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/10),
            ("", self.screen.get_width()/2 - 600, self.screen.get_height()/5),
            ("pygame-gui.Connection_mode", self.screen.get_width()/2 - 600, self.screen.get_height() - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height() - 200),
            ("pygame-gui.Play", self.screen.get_width()/2 - 375, self.screen.get_height() - 100),
            ("pygame-gui.Back", self.screen.get_width()/2 + 125, self.screen.get_height() - 100),
        ]
        self.select_menu_elements_list = []
        # Create buttons and labels and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.select_menu_elements):
            if i == 5 or i == 6: self.select_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, element_text, self.selection_menu_manager))
            elif i == 0 or i == 3: self.select_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), 50, element_text, self.selection_menu_manager))
            elif i == 1:
                try: self.select_menu_elements_list.append(gui.create_drop_down(self.presets_list, self.presets_list[0], x_position, y_position, 400, 50, self.selection_menu_manager))
                except IndexError: self.select_menu_elements_list.append(gui.create_drop_down(['pygame-gui.Error_presets'], 'pygame-gui.Error_presets', x_position, y_position, 400, 50, self.selection_menu_manager))
            elif i == 4: self.select_menu_elements_list.append(gui.create_button(x_position, y_position, 400, 50, self.check_tf_button(self.offline_mode), self.selection_menu_manager))
            else: self.select_menu_elements_list.append(gui.create_text_box(self.descriptions_list[0], x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 600), self.screen.get_height()/2, self.selection_menu_manager))
    def create_options_menu_gui(self):
        # Definición de los botones de opciones
        self.options_menu_buttons = [
            ("pygame-gui.General", self.screen.get_width()/2 - 100, self.screen.get_height()/2 - 200),
            ("pygame-gui.Video", self.screen.get_width()/2 - 100, self.screen.get_height()/2- 140),
            ("pygame-gui.Audio", self.screen.get_width()/2 - 100, self.screen.get_height()/2 - 80),
            ("pygame-gui.Controls", self.screen.get_width()/2 - 100, self.screen.get_height()/2 - 20),
            ("pygame-gui.Back", self.screen.get_width()/2 - 100, self.screen.get_height() - 100),
        ]
        self.options_menu_button = []
        # Create buttons and update their positions
        for element_text, x_position, y_position in self.options_menu_buttons:
            self.options_menu_button.append(gui.create_button(x_position, y_position, 200, 50, element_text, self.options_menu_manager))
    def create_general_options_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.general_options_menu_elements = [
            ("pygame-gui.Language", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("pygame-gui.Font_size", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
            ("pygame-gui.Planet_size", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 80),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 80),
            ("pygame-gui.Advanced_data", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 20),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 20),
            ("pygame-gui.FPS", self.screen.get_width()/2 - 500, self.screen.get_height()/2 + 40),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 + 40),
            ("pygame-gui.Back", self.screen.get_width()/2 - 100, self.screen.get_height() - 100),
        ]
        self.general_options_menu_elements_list = []
        # Create buttons and labels and update their positions
        for i, (element_text, x_position, y_position) in enumerate(self.general_options_menu_elements):
            if i == 10: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 200, 50, element_text, self.general_options_menu_manager))
            elif i%2 == 0: self.general_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 500), 50, element_text, self.general_options_menu_manager))
            elif i == 1:
                if self.language == 'en': language = 'pygame-gui.English'
                elif self.language == 'es': language = 'pygame-gui.Spanish'
                # Create the dropdown menu
                self.general_options_menu_elements_list.append(gui.create_drop_down(self.languages_list, language, x_position, y_position, 250, 50, self.general_options_menu_manager))
            elif i == 7: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_advanced_data), self.general_options_menu_manager))
            elif i == 9: self.general_options_menu_elements_list.append(gui.create_button(x_position, y_position, 250, 50, self.check_tf_button(self.show_FPS), self.general_options_menu_manager))
            else: self.general_options_menu_elements_list.append(gui.create_label(x_position, y_position, 250, 50, element_text, self.general_options_menu_manager))
    def create_video_options_menu_gui(self):
        # Definición de los elementos (botones y etiquetas)
        self.video_options_menu_elements = [
            ("pygame-gui.Resolution", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("pygame-gui.Fullscreen", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
            ("pygame-gui.Back", self.screen.get_width()/2 - 100, self.screen.get_height() - 100),
        ]
        self.video_options_menu_elements_list = []
        for i, (element_text, x_position, y_position) in enumerate(self.video_options_menu_elements):
            if i == 4: self.video_options_menu_elements_list.append(gui.create_button(x_position, y_position, 200, 50, element_text, self.video_options_menu_manager))
            elif i%2 == 0: self.video_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 500), 50, element_text, self.video_options_menu_manager))
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
            ("pygame-gui.Music_volume", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 200),
            ("", self.screen.get_width()/2, self.screen.get_height()/2 - 200),
            ("pygame-gui.Gui_volume", self.screen.get_width()/2 - 500, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2 + 200, self.screen.get_height()/2 - 140),
            ("", self.screen.get_width()/2, self.screen.get_height()/2 - 140),
            ("pygame-gui.Back", self.screen.get_width()/2 - 100, self.screen.get_height() - 100),
        ]
        self.audio_options_menu_elements_list = []
        for i, (element_text, x_position, y_position) in enumerate(self.audio_options_menu_elements):
            if i == 6: self.audio_options_menu_elements_list.append(gui.create_button(x_position, y_position, 200, 50, element_text, self.audio_options_menu_manager))
            elif i == 0 or i == 3: self.audio_options_menu_elements_list.append(gui.create_label(x_position, y_position, (self.screen.get_width()/2 + 200) - (self.screen.get_width()/2 - 500), 50, element_text, self.audio_options_menu_manager))
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
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            sfx.play_sound('menu_move', self.sfx_database)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    def draw_background(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background,(0,0))
    # Método del menú principal del juego
    def main_menu(self):
        while True:
            time_delta = self.clock.tick(60) / 1000.0    
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    sfx.play_sound('menu_change', self.sfx_database)
                    if event.ui_element == self.main_menu_button[0]:
                        self.select()
                    if event.ui_element == self.main_menu_button[1]:
                        self.options()
                    if event.ui_element == self.main_menu_button[3]:
                        pygame.quit()
                        sys.exit()

                self.main_menu_manager.process_events(event)

            self.main_menu_manager.update(time_delta)
            self.draw_background()
            self.main_menu_manager.draw_ui(self.screen)
            pygame.display.update()
    # Método para la selección de sistema
    def select(self):
        running = True 
        while running:
            time_delta = self.clock.tick(60) / 1000.0       
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.video_options_menu_elements_list[4]:
                        self.offline_mode = not self.offline_mode
                        self.select_menu_elements_list[4].set_text(self.check_tf_button(self.offline_mode))  
                    if event.ui_element == self.select_menu_elements_list[5]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        for i, preset_name in enumerate(self.presets_list):
                            if self.select_menu_elements_list[1].selected_option == preset_name:
                                s = CustomPreset(self, entity_data=self.presets_dictionary[self.presets_file_names[i]]["entity_data"])
                                s.start(self)
                                running = False
                    if event.ui_element == self.select_menu_elements_list[6]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                    webbrowser.open_new_tab(event.link_target)
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('menu_select', self.sfx_database)
                    for i, preset_name in enumerate(self.presets_list):
                        if event.text == preset_name:
                            self.select_menu_elements_list[2].set_text(self.descriptions_list[i])   

                self.selection_menu_manager.process_events(event)

            self.selection_menu_manager.update(time_delta) 
            self.draw_background()
            self.selection_menu_manager.draw_ui(self.screen)
            pygame.display.update()
    # Método para la pantalla de opciones
    def options(self):
        running = True 
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.options_menu_button[0]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        self.options_general()
                    if event.ui_element == self.options_menu_button[1]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        self.options_video()
                    if event.ui_element == self.options_menu_button[2]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        self.options_audio()
                    if event.ui_element == self.options_menu_button[3]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        self.options_controls()
                    if event.ui_element == self.options_menu_button[4]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False

                self.options_menu_manager.process_events(event)

            self.options_menu_manager.update(time_delta)
            self.draw_background()
            self.options_menu_manager.draw_ui(self.screen)
            pygame.display.update()
    # Método para la configuración de opciones generales
    def options_general(self):
        running = True 
        while running:
            time_delta = self.clock.tick(60) / 1000.0       
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.general_options_menu_elements_list[7]:
                        self.show_advanced_data = not self.show_advanced_data
                        self.general_options_menu_elements_list[7].set_text(self.check_tf_button(self.show_advanced_data))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS))
                    if event.ui_element == self.general_options_menu_elements_list[9]:
                        self.show_FPS = not self.show_FPS
                        self.general_options_menu_elements_list[9].set_text(self.check_tf_button(self.show_FPS))
                        GeneralSettings.save_general_settings(GeneralSettings(self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS))
                    if event.ui_element == self.general_options_menu_elements_list[10]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                    else: sfx.play_sound('menu_select', self.sfx_database)
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('menu_select', self.sfx_database)
                    if event.text == 'pygame-gui.English':
                        self.set_locale('en')
                    elif event.text == 'pygame-gui.Spanish':
                        self.set_locale('es')
                    GeneralSettings.save_general_settings(GeneralSettings(self.language, self.font_size, self.planet_size, self.show_advanced_data, self.show_FPS))
                self.general_options_menu_manager.process_events(event)

            self.general_options_menu_manager.update(time_delta)
            self.draw_background()
            self.general_options_menu_manager.draw_ui(self.screen)
            pygame.display.update()
    # Método para la configuración de opciones de video
    def options_video(self):
        running = True 
        while running:
            time_delta = self.clock.tick(60) / 1000.0       
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.video_options_menu_elements_list[3]:
                        self.change_fullscreen()
                        self.video_options_menu_elements_list[3].set_text(self.check_tf_button(self.fullscreen))  
                    if event.ui_element == self.video_options_menu_elements_list[4]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                    else: sfx.play_sound('menu_select', self.sfx_database)
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    sfx.play_sound('menu_select', self.sfx_database)
                    if event.text == 'pygame-gui.Native':
                        self.current_resolution = self.resolution_fullscreen
                    elif event.text == '1600x800':
                        self.current_resolution = self.resolution_windowed_1600_800
                    elif event.text == '1280x720':
                        self.current_resolution = self.resolution_windowed_1280_720
                    self.change_resolution()
                self.video_options_menu_manager.process_events(event)

            self.video_options_menu_manager.update(time_delta)
            self.draw_background()
            self.video_options_menu_manager.draw_ui(self.screen)
            pygame.display.update()
    # Método para la configuración de opciones de audio
    def options_audio(self):
        running = True 
        while running:
            time_delta = self.clock.tick(60) / 1000.0       
            for event in pygame.event.get():
                self.check_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.audio_options_menu_elements_list[1]:
                        self.change_music_volume(round(event.value/100, 2))
                        self.audio_options_menu_elements_list[2].set_text(str(int(self.music_volume*100)))
                    if event.ui_element == self.audio_options_menu_elements_list[4]:
                        self.change_gui_volume(round(event.value/100, 2))
                        self.audio_options_menu_elements_list[5].set_text(str(int(self.gui_volume*100)))
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.audio_options_menu_elements_list[6]:
                        sfx.play_sound('menu_change', self.sfx_database)
                        running = False
                self.audio_options_menu_manager.process_events(event)

            self.audio_options_menu_manager.update(time_delta)
            self.draw_background()
            self.audio_options_menu_manager.draw_ui(self.screen)
            pygame.display.update()
    """
    # Método para la configuración de controles
    def options_controls(self):
        running = True
        while running:
            # Definición de los botones de opciones de video
            buttons = [
                ("", self.screen.get_width()/2, self.screen.get_height()/2 - 100),
                ("", self.screen.get_width()/2, self.screen.get_height()/2- 20),
                ("", self.screen.get_width()/2, self.screen.get_height()/2 + 60),
                ("Atrás", self.screen.get_width()/2, self.screen.get_height() - 100),
            ]
            button_rects = self.stablish_hitbox(buttons)
            # Dibujar elementos en la pantalla de opciones de video
            self.draw_header("Controles")
            mx, my = pygame.mouse.get_pos()

            # Dibujar botones y detectar interacción del usuario
            self.draw_buttons(buttons)
            self.reset_menu()
            running = self.check_sub_menu_events(running)  
        
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint((mx, my)):
                    self.index = i
                    if not self.hover_sound_played:
                        sfx.play_sound('menu_move', self.sfx_database)
                        self.hover_sound_played = True
                        self.to_hover = True
                    else:
                        self.to_hover = True
                    if self.click:
                        sfx.play_sound('menu_change', self.sfx_database)
                        if i == 3: running = False
            if not self.to_hover:
                self.hover_sound_played = False
            # Actualización de la pantalla
            self.check_cursor()
            pygame.display.update()
            self.mainClock.tick(60)
            
    # Método para la pantalla de créditos
    def credits(self):
        running = True
        while running:
            # Definición de los botones de la pantalla de créditos
            buttons = [
                ("Atrás", self.screen.get_width()/2, self.screen.get_height() - 100),
            ]
            button_rects = self.stablish_hitbox(buttons)
            # Dibujar elementos en la pantalla de créditos
            self.draw_header("Créditos")
            mx, my = pygame.mouse.get_pos()

            # Dibujar botones y detectar interacción del usuario
            self.draw_buttons(buttons)
            self.reset_menu()
            running = self.check_sub_menu_events(running)  
        
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint((mx, my)):
                    self.index = i
                    if not self.hover_sound_played:
                        sfx.play_sound('menu_move', self.sfx_database)
                        self.hover_sound_played = True
                        self.to_hover = True
                    else:
                        self.to_hover = True
                    if self.click:
                        sfx.play_sound('menu_change', self.sfx_database)
                        if i == 0: running = False
            if not self.to_hover:
                self.hover_sound_played = False
            # Actualización de la pantalla
            self.check_cursor()
            pygame.display.update()
            self.mainClock.tick(60)
"""