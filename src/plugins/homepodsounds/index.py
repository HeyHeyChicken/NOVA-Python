import os
from playsound import playsound
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class HomePodSounds:

    def __init__(self, processor: Processor, tts, events: Events):
        self.tts = tts

        processor.addAction("none", self.none)

        events.onTrigger += self.trigger

    def trigger(self):
        listenPath: str = os.path.join(os.path.dirname(__file__), "mp3", "listen.mp3")
        playsound(listenPath)

    def none(self, intent: Intent, result: ProcessorResult):
        nonePath: str = os.path.join(os.path.dirname(__file__), "mp3", "invalid.mp3")
        playsound(nonePath)