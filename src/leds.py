
import time
from src.libraries.pixel_ring.pixel_ring import PixelRing
from gpiozero import LED

class Leds:
    def __init__(self):
        self.pixelRing = PixelRing()
        power = LED(5)
        power.on()

    def booted(self):
        index: int = 1
        while(index <= 200):
            max: int = 100
            real: int = index
            if real > max:
                real = max - (real - max)

            print(self.pixelRing)
                
            self.pixelRing.set_brightness(real)
            self.pixelRing.set_color(r=255, g=255, b=255)
            time.sleep(0.1)
            index += 1