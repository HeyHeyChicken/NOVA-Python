import os
import random
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.MP3 import MP3

class Random:
    def __init__(self, processor: Processor, mp3: MP3, tts, events: Events, settings):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("random.dice", self.randomDice)
        processor.addAction("random.between", self.randomBetween)

    def randomDice(self, intent: Intent, result: ProcessorResult):
        intent.variables["result"] = self.__random(1, 6)
        self.tts(intent.answer())

    def randomBetween(self, intent: Intent, result: ProcessorResult):
        intent.variables["result"] = self.__random(int(intent.variables['first']), int(intent.variables['last']))
        self.tts(intent.answer())

    def __random(self, first_number, last_number) -> int:
        smaller = first_number if first_number < last_number else last_number
        bigger = last_number if last_number > first_number else first_number
        return random.randint(smaller, bigger)
        