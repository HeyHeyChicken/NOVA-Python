import os
from threading import Thread
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.MP3 import MP3

class HomePodSounds:

    def __init__(self, processor: Processor, mp3: MP3, tts, events: Events, settings):
        self.mp3 = mp3

        processor.addAction("none", self.__none)

        events.onTrigger += self.__trigger
        events.onBooted += self.__booted

    def __playMP3(self, nothing, mp3Path: str):
        self.mp3(mp3Path)

    def __booted(self):
        bootPath: str = os.path.join(os.path.dirname(__file__), "mp3", "boot.mp3")
        Thread(target=self.__playMP3, args=([], bootPath)).start()

    def __trigger(self):
        listenPath: str = os.path.join(os.path.dirname(__file__), "mp3", "listen.mp3")
        Thread(target=self.__playMP3, args=([], listenPath)).start()

    def __none(self, intent: Intent, result: ProcessorResult):
        nonePath: str = os.path.join(os.path.dirname(__file__), "mp3", "invalid.mp3")
        Thread(target=self.__playMP3, args=([], nonePath)).start()