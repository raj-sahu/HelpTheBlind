from gtts import gTTS
import os

language = 'en'
speech = gTTS(text=" ", lang=language, slow=False, tld='co.in')


def describeCaptionAsAudio(text="Caption is Empty"):
    speech.text = text
    speech.save("Description.mp3")
    # Use vlc as mp3 player
    try:
        os.system('cvlc --play-and-exit Description.mp3')
    except:
        print("[ Error Playing Audio CHECK IF CVLC IS INSTALLED ]")


if __name__ == '__main__':
    describeCaptionAsAudio()
