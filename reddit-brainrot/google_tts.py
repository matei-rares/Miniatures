import os
from gtts import gTTS
import subprocess

def generate_tts(text="What's the stupidest thing the most intelligent person in your life believes?",audio_filename="audio_tts.mp3"):

    tts_us = gTTS(text, lang='en', tld='us')

    tts_us.save(f"{audio_filename}.mp3")

    temp_file = "us_temp.mp3"

    cmd = [
        "ffmpeg",
        "-i", audio_filename,
        "-filter:a", "atempo=1.25",
        "-vn",
        temp_file,
        "-y"
    ]

    subprocess.run(cmd, check=True)
    os.replace(temp_file, audio_filename)


