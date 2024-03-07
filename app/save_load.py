import pickle

class GeneralSettings:
    def __init__(self, language='es', font_size='32', planet_size='real', advanced_data=False, show_FPS=True):
        self.language = language
        self.font_size = font_size
        self.planet_size = planet_size
        self.advanced_data = advanced_data
        self.show_FPS = show_FPS

    def save_general_settings(self):
        with open('data/general_settings.dat', 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_general_settings(cls):
        try:
            with open('data/general_settings.dat', 'rb') as file:
                try:
                    general_settings = pickle.load(file)
                    return general_settings.language, general_settings.font_size, general_settings.planet_size, general_settings.advanced_data, general_settings.show_FPS
                except pickle.UnpicklingError:
                    return 'es', '32', 'real', False, True
        except FileNotFoundError:
            return 'es', '32', 'real', False, True

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