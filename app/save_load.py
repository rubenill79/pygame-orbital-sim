import pickle

class GeneralSettings:
    def __init__(self, language='es', gui_scale=100, show_FPS=True, advanced_data=False):
        self.language = language
        self.gui_scale = gui_scale
        self.show_FPS = show_FPS
        self.advanced_data = advanced_data

    def save_general_settings(self):
        try:
            with open('data/general_settings.dat', 'wb') as file:
                pickle.dump(self, file)
        except PermissionError: return

    @classmethod
    def load_general_settings(cls):
        try:
            with open('data/general_settings.dat', 'rb') as file:
                try: 
                    general_settings = pickle.load(file)
                    try: return general_settings.language, general_settings.gui_scale, general_settings.show_FPS, general_settings.advanced_data
                    except AttributeError: pass
                except pickle.UnpicklingError: pass
        except FileNotFoundError: pass
        return 'es', 100, True, False

class SimSettings:
    def __init__(self, distance_mag='AU', angle_mag='Deg', mass_mag='Kg', density_mag='kg/UA', planet_size=1, enable_mouse_hover=True):
        self.distance_mag = distance_mag
        self.angle_mag = angle_mag
        self.mass_mag = mass_mag
        self.density_mag = density_mag
        self.planet_size = planet_size
        self.enable_mouse_hover = enable_mouse_hover
        
    def save_sim_settings(self):
        with open('data/sim_settings.dat', 'wb') as file:
            pickle.dump(self, file)
        
    @classmethod
    def load_sim_settings(cls):
        try:
            with open('data/sim_settings.dat', 'rb') as file:
                try: 
                    sim_settings = pickle.load(file)
                    try: return sim_settings.distance_mag, sim_settings.angle_mag, sim_settings.mass_mag, sim_settings.density_mag, sim_settings.planet_size, sim_settings.enable_mouse_hover
                    except AttributeError: pass
                except pickle.UnpicklingError: pass
        except FileNotFoundError: pass
        return 'AU', 'Deg', 'Kg', 'kg/UA', 1, True

class VideoSettings:
    def __init__(self, fullscreen=False, current_resolution=(1280,720)):
        self.fullscreen = fullscreen
        self.current_resolution = current_resolution

    def save_video_settings(self):
        with open('data/video_settings.dat', 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_video_settings(cls):
        try:
            with open('data/video_settings.dat', 'rb') as file:
                try:
                    video_settings = pickle.load(file)
                    return video_settings.fullscreen, video_settings.current_resolution
                except pickle.UnpicklingError:
                    return False, (1280,720)
        except FileNotFoundError:
            return False, (1280,720)
        
class AudioSettings:
    def __init__(self, music_volume=0.1, gui_volume=0.4):
        self.music_volume = music_volume
        self.gui_volume = gui_volume

    def save_audio_settings(self):
        with open('data/audio_settings.dat', 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_audio_settings(cls):
        try:
            with open('data/audio_settings.dat', 'rb') as file:
                try:
                    audio_settings = pickle.load(file)
                    return audio_settings.music_volume, audio_settings.gui_volume
                except pickle.UnpicklingError:
                    return 0.1, 0.4
        except FileNotFoundError:
            return 0.1, 0.4