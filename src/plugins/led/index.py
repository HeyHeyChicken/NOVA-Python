from events import Events
from src.NaturalLanguage.Processor import Processor
from src.MP3 import MP3
import time
from src.libraries.pixel_ring.pixel_ring import PixelRing

class Led:

    def __init__(self, processor: Processor, mp3: MP3, tts, events: Events, settings):
        self.pixelRing = PixelRing()
        self.booting: bool = False

        events.onBooting += self.__booting
        events.onBooted += self.__booted

    def __booting(self):
        self.booting = True
        index: int = 0
        while(self.booting):
            if index >= 12:
                index = 0
            self.pixelRing.set_color(r=0, g=0, b=0)
            self.pixelRing.set_led_color(255, 255, 255, index)
            time.sleep(0.1)
            index += 1

    def __booted(self):
        self.booting = False
        index: int = 1
        while(index < 200):
            max: int = 100
            real: int = index
            if real > max:
                real = max - (real - max)
                
            self.pixelRing.set_brightness(real)
            self.pixelRing.set_color(r=255, g=255, b=255)
            time.sleep(0.01)
            index += 1