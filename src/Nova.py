import sounddevice
import vosk
from vosk import SetLogLevel
import queue
import json
import sys
import os
from threading import Thread
import struct
import pyaudio
from events import Events
import pvporcupine
from print_color import print
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
from src.TTS import TTS
from src.Audio import Audio
from gpiozero import LED as GPIO_LED

#region Plugins imports

from src.plugins.timer.index import Timer
from src.plugins.chatbot.index import ChatBot
from src.plugins.datedaytimeyear.index import DateDayTimeYear
from src.plugins.deviceipaddress.index import DeviceIPAddress
from src.plugins.mediastack.index import MediaStack
from src.plugins.count.index import Count
from src.plugins.homepodsounds.index import HomePodSounds
from src.plugins.random.index import Random
from src.plugins.volume.index import Volume
from src.plugins.led.index import Led

#endregion

class Nova:
    def __init__(self, rootPath: str):
        self.events = Events()
        self.model = None
        self.samplerate = None
        self.q = queue.Queue()
        self.dump_fn = None
        self.device = None
        self.audio = Audio()
        self.tts = TTS(self.audio, True)
        self.naturalLanguageProcessor = Processor()
        self.microMode: int = 1 # 0 = nothing, 1 = keyword, 2 = listening
        #self.haveWakeWordDetection: bool = False

        settingsPath = os.path.join(rootPath, "settings.json")
        self.settings = json.load(open(settingsPath, encoding='utf-8'))

        power = GPIO_LED(5)
        power.on()

        #region Plugins loading

        pluginsDirectory: str = "plugins"
        for filename in os.listdir(pluginsDirectory):
            f = os.path.join(pluginsDirectory, filename)
            # checking if it is a file
            print(f)

        DateDayTimeYear(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        MediaStack(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        ChatBot(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        DeviceIPAddress(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        Random(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        Count(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        Timer(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        HomePodSounds(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        Volume(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)
        Led(self.naturalLanguageProcessor, self.audio, self.TTS, self.events, self.settings)

        #endregion

        if self.settings["porcupine"]["key"] == "":
            self.print("Please define in '/settings.json file > porcupine > key' the Porcupine key.", "red")
            self.print("You can get one for free from Picovoice Console (https://console.picovoice.ai/)", "red")
            return

        porcupinePath: str = os.path.join(rootPath, "src", "porcupine")
        self.porcupine = pvporcupine.create(
            access_key=self.settings["porcupine"]["key"],
            keyword_paths=[os.path.join(porcupinePath, "WakeWord_Ok-NOVA_fr_" + self.settings["os"] + ".ppn")],
            model_path=os.path.join(porcupinePath, "porcupine_params_fr.pv")
        )

        pyAudio = pyaudio.PyAudio()
        audioStream = pyAudio.open(
            rate = self.porcupine.sample_rate,
            channels = 1,
            format = pyaudio.paInt16,
            input = True,
            frames_per_buffer = self.porcupine.frame_length
        )
        info = pyAudio.get_default_input_device_info()

        Thread(target=self.events.onBooting).start()
        
        self.print("Welcome to NOVA!")
        try:
            deviceInfo = sounddevice.query_devices(info['name'])
        except:
            self.print("No input device found.", "red")
            return

        self.samplerate = int(deviceInfo['default_samplerate'])

        self.print("Speech to text model loading...")
        modelFolderPath: str = os.path.join(rootPath, "src", "models", "model")
        if not os.path.exists(modelFolderPath):
            self.print("In order to understand what you are telling it, NOVA (using Vosk) needs a model.", "red")
            self.print("You can download one of them here : https://alphacephei.com/vosk/models", "red")
            self.print("After downloading, unzip the contents of your model's archive here : /src/models/model/*", "red")
            return
        SetLogLevel(-1)
        self.model = vosk.Model("src/models/model")
        self.print("Speech to text model loaded.")

        Thread(target=self.events.onBooted).start()

        with sounddevice.RawInputStream(samplerate=self.samplerate, blocksize = self.porcupine.frame_length, device=self.device, dtype='int16', channels=1, latency='high', callback=self.callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(self.model, self.samplerate)
            while True:
                if self.microMode == 1:
                    pcm = audioStream.read(self.porcupine.frame_length, exception_on_overflow = False)
                    pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    keyword_index = self.porcupine.process(pcm)
                    if keyword_index >= 0:
                        Thread(target=self.events.onTrigger).start()
                        self.audio.pauseAll()
                        self.microMode = 2

                if self.microMode == 2:
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
        if self.microMode == 2:
            self.q.put(bytes(indata))

    def processTextFromUser(self, text: str):
        """ This function is triggered when the user has finished his sentence. """
        self.print("<- " + text, "white")

        back: ProcessorResult = self.naturalLanguageProcessor.process(text)
        Thread(target=self.events.onProcessed).start()
        self.microMode = 1
        if back.intent != "none":
            if back.answer != None:
                self.microMode = 0
                self.TTS(back.answer)

    def TTS(self, message):
        self.print("-> " + message)
        self.tts.TTS(message, self.TTSFinish)

    def TTSFinish(self):
        self.microMode = 1

    def print(self, message, tagColor: str = "green"):
        print(message, tag='NOVA', tag_color=tagColor, color='white')