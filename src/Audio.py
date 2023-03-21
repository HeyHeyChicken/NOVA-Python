import sys, os
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = sys.__stdout__

class Audio:
    def play(self, path: str):
        pygame.mixer.init()
        print(path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()