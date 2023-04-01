from events import Events
from src.NaturalLanguage.Processor import Processor
from src.Audio import Audio
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.ProcessorResult import ProcessorResult
import time
from src.libraries.pixel_ring.pixel_ring import PixelRing

class Plugin:
    def __init__(self, processor: Processor, mp3: Audio, tts, events: Events, settings):
        self.pixelRing = PixelRing()
        self.booting: bool = False

        processor.addAction("none", self.__none)

        events.onBooting += self.__booting
        events.onBooted += self.__booted
        events.onTrigger += self.__trigger
        events.onProcessed += self.__processed

    def __processed(self):
        self.pixelRing.set_color(r=0, g=0, b=0)

    def __trigger(self):
        self.pixelRing.set_color(r=255, g=255, b=255)
        self.pixelRing.set_brightness(10)

    def __none(self, intent: Intent, result: ProcessorResult):
        time.sleep(0.1)
        self.__once(255, 0, 0, 0.002)
        
    def __booting(self):
        self.booting = True
        index: int = 0
        while(self.booting):
            if index >= 12:
                index = 0
            self.pixelRing.set_color(r=0, g=0, b=0)
            self.pixelRing.set_led_color(255, 255, 255, index)
            self.pixelRing.set_brightness(100)
            time.sleep(0.1)
            index += 1

    def __booted(self):
        time.sleep(0.6)
        self.booting = False
        self.__once(255, 255, 255, 0.01)

    def __once(self, r, g, b, sleep):
        index: int = 1
        while(index < 200):
            max: int = 100
            real: int = index
            if real > max:
                real = max - (real - max)
            self.pixelRing.set_brightness(real)
            self.pixelRing.set_color(r=r, g=g, b=b)
            time.sleep(sleep)
            index += 1
        self.pixelRing.set_color(r=0, g=0, b=0)
        self.pixelRing.set_brightness(100)