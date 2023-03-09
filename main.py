import os

from src.ModuleManager import ModuleManager
moduleManager = ModuleManager()

from src.Nova import Nova
nova = Nova(os.path.dirname(os.path.abspath(__file__)))