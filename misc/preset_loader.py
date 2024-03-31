import os
import json

class PresetReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_json(self):
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def get_data(self):
        return self.data

def load_presets(path):
    preset_files = os.listdir(path)
    presets_database = {}
    preset_file_names = []
    for preset in preset_files:
        reader = PresetReader(path + preset)
        try:
            reader.read_json()
        except PermissionError:
            continue
        name = preset.split('.')[0]
        preset_file_names.append(name)
        presets_database[name] = reader.get_data()
    return presets_database, preset_file_names

def get_presets_name(presets_dictionary):
    global_names = []
    for preset_name, preset_data in presets_dictionary.items():  # Access both key and value
        name = preset_data['global']['global_name']  # Access 'global_name' directly from preset_data
        global_names.append(name)
    return global_names

def get_presets_description(presets_dictionary):
    global_descriptions = []
    for preset_name, preset_data in presets_dictionary.items():  # Access both key and value 
        description = preset_data['global']['global_description']  # Access 'global_name' directly from preset_data
        global_descriptions.append(description)
    return global_descriptions

# Function to get translated text for pygame blit text elements
def get_localized_text(key, language):
    translations_file = f'data/translations/pygame-gui.{language}.json'
    with open(translations_file, 'r', encoding="utf-8") as file:
        translations = json.load(file)
    if language in translations and key in translations[language]:
        return translations[language][key]
    else:
        return key  # Return the key if translation not found