import os
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class HomePodSounds:

    def __init__(self, processor: Processor, tts):
        self.tts = tts