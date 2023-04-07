from vlc import MediaPlayer
from vlc import EventType

class Audio:
    mixers = []

    def play(self, path: str, callback = None):
        player = MediaPlayer(path)
        player.event_manager().event_attach(EventType.MediaPlayerStopped, self.onEnd, callback)
        self.mixers.append(player)
        player.play()
        """
        pygame.init()
        mixer = pygame.mixer
        mixer.init()
        mixer.music.load(path)
        mixer.music.set_volume(1)

        self.mixers.append(mixer)
        mixer.music.play()
        """

    def pauseAll(self):
        for mixer in self.mixers:
            #mixer.music.pause()
            mixer.pause()

    def onEnd(self, event, callback):
        if(callback != None):
            callback()