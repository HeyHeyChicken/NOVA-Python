import os
import socket
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.Audio import Audio

class Plugin:
    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("deviceipaddress.get", self.deviceIPAddressGet)

    def deviceIPAddressGet(self, intent: Intent, result: ProcessorResult):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
 
        intent.variables["address"] = s.getsockname()[0]
        self.tts(intent.answer())
        