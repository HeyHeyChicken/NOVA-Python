
import time
from src.libraries.pixel_ring.pixel_ring import PixelRing

class LED:
    def __init__(self):
        self.pixelRing = PixelRing()

    def booted(self):
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