from gtts import gTTS
from mutagen.mp3 import MP3
import os

def readschedule():
    file = 'test.mp3'
    tts = gTTS(text="You have a meeting at 3 PM. Don't forget to prepare the presentation.", lang='en', slow=False)
    tts.save(file)
    os.system("afplay " + file)
    return get_duration(file)

def get_duration(file):
    audio = MP3(file)
    return audio.info.length


readschedule()