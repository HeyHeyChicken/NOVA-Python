import os
from events import Events
from src.NaturalLanguage.Processor import Processor
from src.Audio import Audio

class ChatBot:
    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))