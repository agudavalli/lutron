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


def readschedule():
    file = 'test.mp3'
    tts = gTTS(text="You have a meeting at 3 PM. Don't forget to prepare the presentation.", lang='en', slow=False)
    tts.save(file)
    os.system("afplay " + file)
    return get_duration(file)

def get_duration(file):
    audio = MP3(file)
    return audio.info.length

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




def take_picture(frame):
    #TODO: Email the photos to the user
    filename = 'captured_image.jpg'
    cv2.imwrite(filename, frame)
    print(f"Image saved as {filename}")
    send_email()
