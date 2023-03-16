import os
from events import Events
from src.NaturalLanguage.Processor import Processor
from src.MP3 import MP3

class ChatBot:
    def __init__(self, processor: Processor, mp3: MP3, tts, events: Events, settings):
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))