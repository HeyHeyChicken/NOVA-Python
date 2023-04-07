from vlc import MediaPlayer
from vlc import EventType
import sys, os
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = sys.__stdout__

class Audio:
    mixers = []

    def play(self, path: str):
        player = MediaPlayer(path)
        player.event_manager().event_attach(EventType.MediaPlayerPlaying, self.onEnd)
        print("start")
        self.mixers.append(player)
        player.play()
        """
        pygame.init();
        mixer = pygame.mixer
        mixer.init()
        mixer.music.load(path)
        mixer.music.set_volume(1)

        self.mixers.append(mixer)
        mixer.music.play()
        """
        print("end")

    def pauseAll(self):
        for mixer in self.mixers:
            #mixer.music.pause()
            mixer.pause()

    def onEnd(self, event):
        print("onEnd:", event.type)