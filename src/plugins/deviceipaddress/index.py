import os
import socket
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class DeviceIPAddress:
    def __init__(self, processor: Processor, tts):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("deviceipaddress.get", self.deviceIPAddressGet)

    def deviceIPAddressGet(self, intent: Intent, result: ProcessorResult):
        intent.variables["address"] = socket.gethostbyname(socket.gethostname())
        self.tts(intent.answer())
        