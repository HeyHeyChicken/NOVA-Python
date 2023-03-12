import os
from threading import Thread
from playsound import playsound
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class HomePodSounds:

    def __init__(self, processor: Processor, tts, events: Events):
        self.tts = tts

        processor.addAction("none", self.__none)

        events.onTrigger += self.__trigger
        events.onBooted += self.__booted

    def __playMP3(self, nothing: list[any], mp3Path: str):
        playsound(mp3Path)

    def __booted(self):
        bootPath: str = os.path.join(os.path.dirname(__file__), "mp3", "boot.mp3")
        Thread(target=self.__playMP3, args=([], bootPath)).start()

    def __trigger(self):
        listenPath: str = os.path.join(os.path.dirname(__file__), "mp3", "listen.mp3")
        Thread(target=self.__playMP3, args=([], listenPath)).start()

    def __none(self, intent: Intent, result: ProcessorResult):
        nonePath: str = os.path.join(os.path.dirname(__file__), "mp3", "invalid.mp3")
        Thread(target=self.__playMP3, args=([], nonePath)).start()