import sys, os
sys.stdout = open(os.devnull, 'w')

import pygame
import aifc

sys.stdout = sys.__stdout__

class Audio:
    def play(self, path: str):
        pygame.mixer.init()
        print(path)
        if path.endswith(".aiff"):
            aifc.open(path, 'r')
        else:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()