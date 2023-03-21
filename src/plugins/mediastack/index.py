import os
import requests
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.Audio import Audio

class MediaStack:
    apiKey: str = ""

    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("mediastack.get.news", self.getNewsAction)
    
    def getNewsAction(self, intent: Intent, result: ProcessorResult):
        """ This function is triggered when the user requests the general information. """
        resp = requests.get(url='http://api.mediastack.com/v1/news?countries=fr&access_key=' + self.apiKey, headers={'Accept': 'application/json'})
        data = resp.json()

        phrase: str = "Voici les dernières actualités : "
        index: int = 0
        for actu in data["data"]:
            if index < 3:
                description: str = actu["description"]
                if description != "":
                    if not description.endswith('...'):
                        phrase += "Selon " + actu["source"] + " : " + description + " "
                        index = index + 1
        self.tts(phrase)