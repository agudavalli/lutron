import smtplib
from email.mime.multipart import MIMEMultipart

from gtts import gTTS
from mutagen.mp3 import MP3
import cv2
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import flashinglights
import subprocess
import random
import sys

#import flashinglightsv2


def readschedule():
    file = 'test.mp3'
    tts = gTTS(text="You have your lutron presentation at 1pm, remember to finish the project", lang='en', slow=False)
    tts.save(file)
    os.system("aplay " + file)

def send_email():
    smtp_server = 'smtp.gmail.com'
    port = 587
    username = 'googlygod420@gmail.com'
    password = 'setk qaac ltxy nmdj'
    to_email = ['abhibg@bu.edu']

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = ', '.join(to_email)
    msg['Subject'] = 'Captured Image'
    body = 'Please find the attached image captured by the camera.'
    msg.attach(MIMEText(body, 'plain'))
    with open('captured_image.jpg', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= captured_image.jpg')
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, to_email, msg.as_string())
    server.quit()




def take_picture():
    #TODO: Add call to lighting for all white LEDS

    filename = 'captured_image.jpg'
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cv2.imwrite(filename, frame)
    print(f"Image saved as {filename}")
    send_email()

def play_song():
    #TODO: Add lighting function
    global _audio_process
    song = random.randint(0,4)
    filename = ''
    if song == 0:
        filename = 'lighters.mp3'
    elif song == 1:
        filename = 'flashinglights.mp3'
        #light function
    elif song == 2:
        filename = 'allofthelights.mp3'
    elif song == 3:
        filename = 'blindinglights.mp3'
    _audio_process = subprocess.Popen(['aplay', filename])

def stop_song():
    global _audio_process
    if _audio_process is not None:
        _audio_process.terminate()
        _audio_process = None
    os.system('aplay what.mp3')

def words_of_affirmation():
    phrase = random.randint(0,5)
    if phrase == 0:
        speech = "You are doing great, keep it up!"
    elif phrase == 1:
        speech = "You are a wonderful person, don't forget that!"
    elif phrase == 2:
        speech = "You are so smart, you can do anything you set your mind to!"
    elif phrase == 3:
        speech = "You are so kind, the world is a better place with you in it!"
    elif phrase == 4:
        speech = "You are so talented, you can achieve anything you want!"
    tts = gTTS(text=speech, lang='en', slow=False)
    filename = 'affirmation.mp3'
    tts.save(filename)
    os.system("aplay " + filename)

def play_flashing_lights():
    global _audio_process
    filename = 'flashinglights.mp3'
    _audio_process = subprocess.Popen(['aplay', filename])

    send_command('all_red')

    #call lighting sequence here
    #flashinglightsv2.flashing_lights_kanye()

def calibrate():
    send_command('all_yellow')

def nether():
    send_command('nether')



def send_command(command):
    command_line = subprocess.Popen(
    ["sudo", "python3", "lighting.py"],
    stdin=subprocess.PIPE,
    text=True
    )
    command_line.stdin.write(command + "\n")
    command_line.stdin.flush()



