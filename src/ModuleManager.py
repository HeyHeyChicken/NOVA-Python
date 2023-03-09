import sys
import subprocess
import pkg_resources

class ModuleManager:
    """ This class is used to check the correct installation of the modules required for the project. """
    def __init__(self):
        self.checkPackages()

    def checkPackages(self):
        """ This function checks that the modules required for the project are installed. If the modules are not installed, they are installed automatically. """
        print("Checking modules installation...")

        # List of modules to install (name/optionnal version)
        packages: dict[str, str] = {
            "print-color": "",
            "vosk": "",
            "sounddevice": "",
            "playsound": "1.2.2",
            "pyobjc": ""
        }
        
        installed = {pkg.key for pkg in pkg_resources.working_set}
        for package in packages:
            print(f"    Checking module {package!r}...")
            if (package in installed):
                print(f"        Module {package!r} is already installed.")
            else:
                print(f"        Module {package!r} isn't installed.")
                print(f"        Installing module {package!r}...")
                packageName: str = package
                packageVersion: str = packages[package]
                if packageVersion != "":
                    packageName += "==" + packageVersion
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', packageName, '--no-warn-script-location'], stdout=subprocess.DEVNULL)
                print(f"        Module {package!r} is now installed.")