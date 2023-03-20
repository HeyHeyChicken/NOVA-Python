from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

class MP3:
    def play(self, path: str):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()