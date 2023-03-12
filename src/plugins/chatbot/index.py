import os
from events import Events
from src.NaturalLanguage.Processor import Processor

class ChatBot:
    def __init__(self, processor: Processor, tts, events: Events, settings):
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))