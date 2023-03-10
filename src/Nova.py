import sounddevice
import vosk
import queue
import json
import sys
import os
from print_color import print
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.TTS import TTS

#region Plugins imports

from src.plugins.chatbot.index import ChatBot
from src.plugins.datedaytimeyear.index import DateDayTimeYear
from src.plugins.deviceipaddress.index import DeviceIPAddress
from src.plugins.mediastack.index import MediaStack
from src.plugins.count.index import Count
from src.plugins.homepodsounds.index import HomePodSounds
from src.plugins.random.index import Random

#endregion

class Nova:        
    def __init__(self, rootPath: str):
        self.model = None
        self.samplerate = None
        self.q = queue.Queue()
        self.dump_fn = None
        self.device = None
        self.tts = TTS()
        self.naturalLanguageProcessor = Processor()
        self.haveToProcess: bool = True

        settingsPath = os.path.join(rootPath, "settings.json")
        self.settings = json.load(open(settingsPath, encoding='utf-8'))

        #region Plugins loading

        DateDayTimeYear(self.naturalLanguageProcessor, self.TTS)
        MediaStack(self.naturalLanguageProcessor, self.TTS)
        ChatBot(self.naturalLanguageProcessor, self.TTS)
        DeviceIPAddress(self.naturalLanguageProcessor, self.TTS)
        Random(self.naturalLanguageProcessor, self.TTS)
        Count(self.naturalLanguageProcessor, self.TTS)
        HomePodSounds(self.naturalLanguageProcessor, self.TTS)

        #endregion
        
        self.print("Welcome to NOVA!")
        try:
            deviceInfo = sounddevice.query_devices(self.settings["audio"]["input"])
        except:
            self.print("No input device matching '" + self.settings["audio"]["input"] + "'.", "red")
            self.print("Here is the list of available devices:", "red")
            print(sounddevice.query_devices())
            self.print("Please define in '/settings.json file > audio > input' the device you want to use as microphone.", "red")
            return

        self.samplerate = int(deviceInfo['default_samplerate'])

        self.print("Speech to text model loading...")
        modelFolderPath: str = os.path.join(rootPath, "src", "models", "model")
        if not os.path.exists(modelFolderPath):
            self.print("In order to understand what you are telling it, NOVA (using Vosk) needs a model.", "red")
            self.print("You can download one of them here : https://alphacephei.com/vosk/models", "red")
            self.print("After downloading, unzip the contents of your model's archive here : /src/models/model/*", "red")
            return
        self.model = vosk.Model("src/models/model")
        self.print("Speech to text model loaded.")

        with sounddevice.RawInputStream(samplerate=self.samplerate, blocksize = 1024, device=self.device, dtype='int16', channels=1, latency='high', callback=self.callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    r = eval(rec.Result())
                    t = r["text"]
                    if t:
                        self.processTextFromUser(t)
                        if self.dump_fn is not None and len(t) > 5:
                            self.dump_fn.write(t+'\n')

    def callback(self, indata, frames, time, status):
        """ This function is triggered when the user speaks. """
        if status:
            print(status, file=sys.stderr)
        if self.haveToProcess:
            self.q.put(bytes(indata))

    def processTextFromUser(self, text: str):
        """ This function is triggered when the user has finished his sentence. """
        self.print("<- " + text, "white")

        back: ProcessorResult = self.naturalLanguageProcessor.process(text)
        if back.intent != "none":
            if back.answer != None:
                self.TTS(back.answer)

    def TTS(self, message):
        self.print("-> " + message)
        self.haveToProcess = False
        self.tts.TTS(message, self.TTSFinish)

    def TTSFinish(self):
        self.haveToProcess = True

    def print(self, message, tagColor: str = "green"):
        print(message, tag='NOVA', tag_color=tagColor, color='white')