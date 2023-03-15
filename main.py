import os
from playsound import playsound

rootPath: str = os.path.dirname(os.path.abspath(__file__))

from src.ModuleManager import ModuleManager
moduleManager = ModuleManager(rootPath)

#from src.Nova import Nova
#nova = Nova(rootPath)

bootPath: str = os.path.join(rootPath, "src", "plugins", "homepodsounds", "mp3", "boot.mp3")
print(bootPath)
playsound(bootPath)