import sys, os
sys.stdout = open(os.devnull, 'w')

import pygame

class MP3:
    def play(self, path: str):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()