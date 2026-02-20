from gtts import gTTS
from mutagen.mp3 import MP3
import cv2
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

def take_picture(frame):
    #TODO: Email the photos to the user
    filename = 'captured_image.jpg'
    cv2.imwrite(filename, frame)
    print(f"Image saved as {filename}")