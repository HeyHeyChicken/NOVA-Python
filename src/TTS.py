from threading import Thread
from urllib.request import urlopen
from pathlib import Path
import os
import datetime
import urllib.parse
from src.Audio import Audio

class TTS:
    url: str = "http://192.168.1.12/api"

    def __init__(self, audio: Audio, mp3: bool = False):
        self.audio: Audio = audio
        self.mp3: bool = mp3

    def TTS(self, message: str, callback):
        folder: str = os.path.join(os.path.dirname(__file__), "audio")
        
        # If the "mp3" folder exists, delete its contents
        if os.path.exists(folder):
            oldFiles: str() = os.listdir(folder)
            for oldFile in oldFiles:
                os.remove(os.path.join(folder, oldFile))

        # We create the folder containing the voice files if it does not exist.
        Path(folder).mkdir(parents=True, exist_ok=True)

        # We are looking for a temporary file name.
        now: datetime = datetime.datetime.now()
        epoch: datetime = datetime.datetime.utcfromtimestamp(0)
        name: int = int((now - epoch).total_seconds() * 1000000)
        
        fileExtension: str = ".aiff"
        if self.mp3:
            fileExtension = ".mp3"

        localFileName: str = os.path.join(folder, str(name) + fileExtension)

        # We download the voice file from the TTS server.
        finalURL: str = self.url + "?sentence=" + urllib.parse.quote(message)
        print(finalURL)
        mp3file = urlopen(finalURL)
        with open(localFileName,'wb') as output:
            output.write(mp3file.read())

        # We play the audio file.
        Thread(target=self.__playMP3, args=([],localFileName, callback)).start()

    def __playMP3(self, nothing, mp3Path: str, callback):
        self.audio.play(mp3Path)
        callback()