import os
import random
import pygame

def load_sfx(path):
    sfx_list = os.listdir(path)
    sfx_database = {}
    for sound in sfx_list:
        sfx_database[sound.split('.')[0]] = pygame.mixer.Sound(path + sound)
    return sfx_database

def play_sound(sfx_id, sfx_database):
    sound = sfx_database[sfx_id]
    if type(sound) == type([]):
        random.choice(sound).play()
    else:
        sound.play()