import vlc
import sys, os
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = sys.__stdout__

class Audio:
    mixers = []

    def play(self, path: str):
        p = vlc.MediaPlayer(path)
        p.play()
        """
        pygame.init();
        mixer = pygame.mixer
        mixer.init()
        mixer.music.load(path)
        mixer.music.set_volume(1)

        self.mixers.append(mixer)
        mixer.music.play()
        """

    def pauseAll(self):
        for mixer in self.mixers:
            mixer.music.pause()