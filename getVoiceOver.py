import pyttsx3 # type: ignore
from getConfig import *

def create_voice_over(fileName, text):
    filePath = f"{get_voice_over_directory()}/{fileName}.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath