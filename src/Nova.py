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

        #region Plugins loading

        DateDayTimeYear(self.naturalLanguageProcessor, self.TTS)
        MediaStack(self.naturalLanguageProcessor, self.TTS)
        ChatBot(self.naturalLanguageProcessor, self.TTS)
        DeviceIPAddress(self.naturalLanguageProcessor, self.TTS)
        Random(self.naturalLanguageProcessor, self.TTS)
        Count(self.naturalLanguageProcessor, self.TTS)
        HomePodSounds(self.naturalLanguageProcessor, self.TTS)

        #endregion
        
        settingsPath = os.path.join(rootPath, "settings.json")
        settings = json.load(open(settingsPath, encoding='utf-8'))
        print(settings)
        
        self.print("Welcome to NOVA!")
        try:
            deviceInfo = sounddevice.query_devices(settings.audio.input)
        except Exception as e:
            self.print(e, "red")
            self.print("Audio input not found.", "red")
            return

        self.samplerate = int(deviceInfo['default_samplerate'])

        self.print("Speech to text model loading...")
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
        self.tts.TTS(message)

    def print(self, message, tagColor: str = "green"):
        print(message, tag='NOVA', tag_color=tagColor, color='white')