import os
from events import Events
from src.NaturalLanguage.Intent import Intent
from src.NaturalLanguage.Processor import Processor
from src.NaturalLanguage.ProcessorResult import ProcessorResult
import time

class Volume:
    integers: list[str] = [
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

    def __init__(self, processor: Processor, tts, events: Events, settings):
        self.tts = tts
        self.settings = settings
        processor.loadJson(os.path.join(os.path.dirname(__file__), "corpus.json"))

        processor.addAction("volume.percent", self.__volumePercent)

    def __volumePercent(self, intent: Intent, result: ProcessorResult):
        percentString: str = intent.variables['percent']
        if percentString in self.integers:
            percentInt: int = self.integers.index(percentString)

            if self.settings["os"] == "mac":
                import osascript
                osascript.osascript("set volume output volume " + str(percentInt))
            elif self.settings["os"] == "raspberry":
                import alsaaudio
                mixer = alsaaudio.Mixer()
                mixer.setvolume(percentInt)
            elif self.settings["os"] == "nt": # Windows
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                
                volumes: list[float] = [
                    -37,    # 0
                    -35,    # 1
                    -34,    # 2
                    -33,    # 3
                    -32,    # 4
                    -31,    # 5
                    -30,    # 6
                    -29,    # 7
                    -28,    # 8
                    -27,    # 9
                    -26,    # 10
                    -25.5,  # 11
                    -25,    # 12
                    -24,    # 13
                    -23.5,  # 14
                    -23,    # 15
                    -22,    # 16
                    -21.5,  # 17
                    -21,    # 18
                    -20.5,  # 19
                    -20,    # 20
                    -19.5,  # 21
                    -19,    # 22
                    -18.5,  # 23
                    -18,    # 24
                    -17.5,  # 25
                    -17,    # 26
                    -16.5,  # 27
                    -16.25, # 28
                    -16,    # 29
                    -15.5,  # 30
                    -15.25, # 31
                    -14.75, # 32
                    -14.5,  # 33
                    -14,    # 34
                    -13.75, # 35
                    -13.25, # 36
                    -13,    # 37
                    -12.75, # 38
                    -12.5,  # 39
                    -12,    # 40
                    -11.75, # 41
                    -11.5,  # 42
                    -11.25, # 43
                    -11,    # 44
                    -10.5,  # 45
                    -10.25, # 46
                    -10,    # 47
                    -9.75,  # 48
                    -9.5,   # 49
                    -9.25,  # 50
                    -9,     # 51
                    -8.75,  # 52
                    -8.5,   # 53
                    -8.25,  # 54
                    -8,     # 55
                    -7.75,  # 56
                    -7.5,   # 57
                    -7.25,  # 58
                    -7.12,  # 59
                    -7,     # 60
                    -6.75,  # 61
                    -6.5,   # 62
                    -6.25,  # 63
                    -6.12,  # 64
                    -5.9,   # 65
                    -5.7,   # 66
                    -5.5,   # 67
                    -5.3,   # 68
                    -5.1,   # 69
                    -4.9,   # 70
                    -4.7,   # 71
                    -4.5,   # 72
                    -4.3,   # 73
                    -4.1,   # 74
                    -3.9,   # 75
                    -3.7,   # 76
                    -3.5,   # 77
                    -3.4,   # 78
                    -3.3,   # 79
                    -3.1,   # 80
                    -2.9,   # 81
                    -2.7,   # 82
                    -2.5,   # 83
                    -2.4,   # 84
                    -2.3,   # 85
                    -2.1,   # 86
                    -1.9,   # 87
                    -1.7,   # 88
                    -1.6,   # 89
                    -1.5,   # 90
                    -1.3,   # 91
                    -1.1,   # 92
                    -1,     # 93
                    -0.9,   # 94
                    -0.7,   # 95
                    -0.5,   # 96
                    -0.4,   # 97
                    -0.3,   # 98
                    -0.12,  # 99
                    0,  # 100
                ]
                volume.SetMasterVolumeLevel(volumes[percentInt], None)

            intent.variables["percent"] = intent.variables['percent']
            self.tts(intent.answer())
        