import os
from events import Events
from threading import Thread
from src.SetTimeOut import SetTimeOut
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.Audio import Audio

class Plugin:
    alarms: bool() = []
    integers: str() = [
        "zéro", "une", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
        "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf",
        "vingt", "vingt et une", "vingt-deux", "vingt-trois", "vingt-quatre", "vingt-cinq", "vingt-six", "vingt-sept", "vingt-huit", "vingt-neuf",
        "trente", "trente et une", "trente-deux", "trente-trois", "trente-quatre", "trente-cinq", "trente-six", "trente-sept", "trente-huit", "trente-neuf",
        "quarante", "quarante et une", "quarante-deux", "quarante-trois", "quarante-quatre", "quarante-cinq", "quarante-six", "quarante-sept", "quarante-huit", "quarante-neuf",
        "cinquante", "cinquante et une", "cinquante-deux", "cinquante-trois", "cinquante-quatre", "cinquante-cinq", "cinquante-six", "cinquante-sept", "cinquante-huit", "cinquante-neuf",
        "soixante", "soixante et une", "soixante-deux", "soixante-trois", "soixante-quatre", "soixante-cinq", "soixante-six", "soixante-sept", "soixante-huit", "soixante-neuf",
        "soixante-dix", "soixante et onze", "soixante-douze", "soixante-treize", "soixante-quatorze", "soixante-quinze", "soixante-seize", "soixante-dix-sept", "soixante-dix-huit", "soixante-dix-neuf",
        "quatre-vingts", "quatre-vingt-une", "quatre-vingt-deux", "quatre-vingt-trois", "quatre-vingt-quatre", "quatre-vingt-cinq", "quatre-vingt-six", "quatre-vingt-sept", "quatre-vingt-huit", "quatre-vingt-neuf",
        "quatre-vingt-dix", "quatre-vingt-onze", "quatre-vingt-douze", "quatre-vingt-treize", "quatre-vingt-quatorze", "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-dix-sept", "quatre-vingt-dix-huit", "quatre-vingt-dix-neuf",
        "cent"
    ]

    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        self.tts = tts
        self.mp3 = mp3
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("timer.minutes", self.__timerMinutes)
        processor.addAction("timer.secondes", self.__timerSecondes)
        processor.addAction("timer.stop", self.__timerStop)
    
    def __timerRing(self, args):
        alarmPath: str = os.path.join(os.path.dirname(__file__), "mp3", "alarm.mp3")
        Thread(target=self.__timerRingLoop, args=(args,alarmPath)).start()
    
    def __timerRingLoop(self, args, alarmPath: str):
        #while(self.alarms[args[0]] == False):
        #    print("play")
        self.mp3.play(alarmPath)
    
    def __timerStop(self, intent: Intent, result: ProcessorResult):
        for index, alarm in enumerate(self.alarms):
            self.alarms[index] = True

    def __timerSecondes(self, intent: Intent, result: ProcessorResult):
        secondesString: str = intent.variables['secondes']
        if secondesString in self.integers:
            secondesInt: int = self.integers.index(secondesString)

            self.__timer(secondesInt * 1000)

            intent.variables["secondes"] = intent.variables['secondes']
            self.tts(intent.answer())

    def __timerMinutes(self, intent: Intent, result: ProcessorResult):
        minutesString: str = intent.variables['minutes']
        if minutesString in self.integers:
            minutesInt: int = self.integers.index(minutesString)

            self.__timer(minutesInt * 60 * 1000)

            intent.variables["minutes"] = intent.variables['minutes']
            self.tts(intent.answer())

    def __timer(self, time: int):
        index: int = -1
        for loopIndex, alarm in enumerate(self.alarms):
            if self.alarms[loopIndex] == True:
                index = loopIndex
        if index < 0:
            index = len(self.alarms)
            self.alarms.append(False)

        SetTimeOut(self.__timerRing, time, [index])







        