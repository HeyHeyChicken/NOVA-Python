import os

rootPath: str = os.path.dirname(os.path.abspath(__file__))

#from src.ModuleManager import ModuleManager
#moduleManager = ModuleManager(rootPath)

from src.Nova import Nova
nova = Nova(rootPath)