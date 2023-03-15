import sys
import os
import json
import subprocess
import pkg_resources

class ModuleManager:
    """ This class is used to check the correct installation of the modules required for the project. """
    def __init__(self, rootPath: str):
        self.settings: None

        self.checkOS(rootPath)
        self.checkPackages()

    def checkOS(self, rootPath: str):
        settingsPath = os.path.join(rootPath, "settings.json")
        self.settings = json.load(open(settingsPath, encoding='utf-8'))

        if self.settings["os"] == "":
            self.settings["os"] = os.name

        if self.settings["os"] == "posix":
            print("In order to configure NOVA, can you tell us the OS you are using?")
            print("1) Raspberry")
            print("2) Mac")
            self.setOSLoop()
        
        with open(settingsPath, 'w') as outfile:
            json.dump(self.settings, outfile)

    def setOSLoop(self):
        strInput: str = input("OS index? (1, 2)")
        if strInput.isdigit():
            intInput: int = int(strInput)
            if intInput == 1:
                self.settings["os"] = "raspberry"
            else:
                if intInput == 2:
                    self.settings["os"] = "mac"
            if self.settings["os"] == "posix":
                print("Please provide an integer between 1 and 2.")
                self.setOSLoop()
        else:
            print("Please provide an integer.")
            self.setOSLoop()

    def checkPackages(self):
        """ This function checks that the modules required for the project are installed. If the modules are not installed, they are installed automatically. """
        print("Checking modules installation...")

        # List of modules to install (name/optionnal version)
        packages: dict[str, str] = {
            "print-color": "",
            "vosk": "",
            "sounddevice": "",
            "playsound": "1.2.2",
            "pvporcupine": "",
            "pyaudio": "",
            "events": "",
        }
        
        for package in packages:
            self.checkPackage(package, packages[package])
        if self.settings["os"] == "mac":
            self.checkPackage("pyobjc", "")
            self.checkPackage("osascript", "")
        elif self.settings["os"] == "raspberry":
            self.checkPackage("pyalsaaudio", "")
        elif self.settings["os"] == "nt": # Windows
            self.checkPackage("pycaw", "")

    def checkPackage(self, package: str, version: str):
        installed = {pkg.key for pkg in pkg_resources.working_set}
        print(f"    Checking module {package!r}...")
        if (package in installed):
            print(f"        Module {package!r} is already installed.")
        else:
            print(f"        Module {package!r} isn't installed.")
            print(f"        Installing module {package!r}...")
            packageName: str = package
            packageVersion: str = version
            if packageVersion != "":
                packageName += "==" + packageVersion
            subprocess.check_call([sys.executable, '-m', 'pip3', 'install', packageName, '--no-warn-script-location'], stdout=subprocess.DEVNULL)
            print(f"        Module {package!r} is now installed.")