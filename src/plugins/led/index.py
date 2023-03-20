from events import Events
from src.NaturalLanguage.Processor import Processor
from src.MP3 import MP3
import time
from src.libraries.pixel_ring.pixel_ring import PixelRing
from gpiozero import LED as GPIO_LED

class Led:

    def __init__(self, processor: Processor, mp3: MP3, tts, events: Events, settings):
        self.pixelRing = PixelRing()
        power = GPIO_LED(5)
        power.on()

        events.onBooted += self.__booted

    def __booted(self):
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