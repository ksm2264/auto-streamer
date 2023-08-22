from elevenlabs import generate, play
from streamer.audio.clone import get_voice

from dotenv import load_dotenv
import os
load_dotenv()

name = os.getenv('CHARACTER_NAME')

class Speaker:

    def __init__(self):

        self.voice = get_voice()

        print(f'loading the voice of {name}')

    def generate_audio(self, text: str) -> bytes:

        audio = generate(text = text, voice = self.voice)

        return audio

if __name__ == "__main__":

    text = "Hi! I'm a cloned voice!"

    speaker = Speaker()

    audio = speaker.generate_audio(text)

    play(audio)