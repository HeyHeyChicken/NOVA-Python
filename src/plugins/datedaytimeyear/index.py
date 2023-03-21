import os
import datetime
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.Audio import Audio

class DateDayTimeYear:
    weekDays: str() = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    months: str() = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("time.get", self.timeGet)
        processor.addAction("date.get", self.dateGet)
        processor.addAction("year.get", self.yearGet)
        processor.addAction("day.get", self.dayGet)

    def dateGet(self, intent: Intent, result: ProcessorResult):
        now: datetime = datetime.datetime.now()
        intent.variables["date"] = self.weekDays[now.weekday()] + " " + str(now.day) + " " + self.months[now.month] + " " + str(now.year)
        self.tts(intent.answer())

    def timeGet(self, intent: Intent, result: ProcessorResult):
        now: datetime = datetime.datetime.now()
        intent.variables["hour"] = now.hour
        intent.variables["minute"] = now.minute
        self.tts(intent.answer())

    def yearGet(self, intent: Intent, result: ProcessorResult):
        now: datetime = datetime.datetime.now()
        intent.variables["year"] = now.year
        self.tts(intent.answer())

    def dayGet(self, intent: Intent, result: ProcessorResult):
        now: datetime = datetime.datetime.now()
        intent.variables["day"] = self.weekDays[now.weekday()]
        self.tts(intent.answer())
        