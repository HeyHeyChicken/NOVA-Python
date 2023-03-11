import os
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult

class Count:
    def __init__(self, processor: Processor, tts, events: Events):
        self.tts = tts
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("count.up", self.countUp)
        processor.addAction("count.down", self.countDown)
        processor.addAction("count.from.to", self.countFromTo)

    def countUp(self, intent: Intent, result: ProcessorResult):
        answer: str = ""
        for index in range(int(intent.variables['number'])):
            nb: int = index + 1
            answer += str(nb)
            if nb < int(intent.variables['number']):
                answer += ", "
            else:
                answer += "."
        self.tts(answer)

    def countDown(self, intent: Intent, result: ProcessorResult):
        answer: str = ""
        inputNumber = int(intent.variables['number']) + 1
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
        answer: str = ""

        inputFrom: int = int(intent.variables['from'])
        inputTo: int = int(intent.variables['to'])

        loopFrom: int = inputFrom if inputFrom < inputTo else inputTo
        loopTo: int = inputTo if inputFrom < inputTo else inputFrom
        loopTo += 1
        
        loopArray = range(loopFrom, loopTo)
        loopList = list(loopArray)
        if inputTo < inputFrom:
            loopList.reverse()

        for index in loopList:
            answer += str(index)
            if index == ((loopTo - 1) if inputFrom < inputTo else loopFrom):
                answer += "."
            else:
                answer += ", "
        self.tts(answer)
        