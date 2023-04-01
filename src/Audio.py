import sys, os
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = sys.__stdout__

class Audio:
    mixers = []

    def play(self, path: str):
        mixer = pygame.mixer
        mixer.init()
        mixer.music.load(path)
        self.mixers.append(mixer)
        mixer.music.play()
        print(self.mixers)