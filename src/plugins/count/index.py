import os
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.Audio import Audio

class Count:
    integers: str() = [
        "zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
        "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf",
        "vingt", "vingt et un", "vingt-deux", "vingt-trois", "vingt-quatre", "vingt-cinq", "vingt-six", "vingt-sept", "vingt-huit", "vingt-neuf",
        "trente", "trente et un", "trente-deux", "trente-trois", "trente-quatre", "trente-cinq", "trente-six", "trente-sept", "trente-huit", "trente-neuf",
        "quarante", "quarante et un", "quarante-deux", "quarante-trois", "quarante-quatre", "quarante-cinq", "quarante-six", "quarante-sept", "quarante-huit", "quarante-neuf",
        "cinquante", "cinquante et un", "cinquante-deux", "cinquante-trois", "cinquante-quatre", "cinquante-cinq", "cinquante-six", "cinquante-sept", "cinquante-huit", "cinquante-neuf",
        "soixante", "soixante et un", "soixante-deux", "soixante-trois", "soixante-quatre", "soixante-cinq", "soixante-six", "soixante-sept", "soixante-huit", "soixante-neuf",
        "soixante-dix", "soixante et onze", "soixante-douze", "soixante-treize", "soixante-quatorze", "soixante-quinze", "soixante-seize", "soixante-dix-sept", "soixante-dix-huit", "soixante-dix-neuf",
        "quatre-vingts", "quatre-vingt-un", "quatre-vingt-deux", "quatre-vingt-trois", "quatre-vingt-quatre", "quatre-vingt-cinq", "quatre-vingt-six", "quatre-vingt-sept", "quatre-vingt-huit", "quatre-vingt-neuf",
        "quatre-vingt-dix", "quatre-vingt-onze", "quatre-vingt-douze", "quatre-vingt-treize", "quatre-vingt-quatorze", "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-dix-sept", "quatre-vingt-dix-huit", "quatre-vingt-dix-neuf",
        "cent"
    ]

    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("count.up", self.countUp)
        processor.addAction("count.down", self.countDown)
        processor.addAction("count.from.to", self.countFromTo)

    def countUp(self, intent: Intent, result: ProcessorResult):
        valueString: str = intent.variables['number']
        if valueString in self.integers:
            valueInt: int = self.integers.index(valueString)
            answer: str = ""

            for index in range(valueInt):
                nb: int = index + 1
                answer += str(nb)
                if nb < valueInt:
                    answer += ", "
                else:
                    answer += "."
            self.tts(answer)

    def countDown(self, intent: Intent, result: ProcessorResult):
        valueString: str = intent.variables['number']
        if valueString in self.integers:
            valueInt: int = self.integers.index(valueString)
            answer: str = ""

            inputNumber = valueInt + 1
            loopArray = range(inputNumber)
            loopList = list(reversed(loopArray))
            for index in loopList:
                answer += str(index)
                if index == 0:
                    answer += "."
                else:
                    answer += ", "
            self.tts(answer)

    def countFromTo(self, intent: Intent, result: ProcessorResult):
        fromString: int = int(intent.variables['from'])
        toString: int = int(intent.variables['to'])
        if fromString in self.integers:
            if toString in self.integers:
                fromInt: int = self.integers.index(fromString)
                toInt: int = self.integers.index(toString)
                answer: str = ""

                loopFrom: int = fromInt if fromInt < toInt else toInt
                loopTo: int = toInt if fromInt < toInt else fromInt
                loopTo += 1
                
                loopArray = range(loopFrom, loopTo)
                loopList = list(loopArray)
                if toInt < fromInt:
                    loopList.reverse()

                for index in loopList:
                    answer += str(index)
                    if index == ((loopTo - 1) if fromInt < toInt else loopFrom):
                        answer += "."
                    else:
                        answer += ", "
                self.tts(answer)
        