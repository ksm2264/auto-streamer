from elevenlabs import clone, set_api_key, voices
import os
import glob
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('ELEVENLABS_API_KEY')
set_api_key(api_key)

name = os.getenv('CHARACTER_NAME')

from streamer.audio.clip import create_clips

def get_voice():
    my_voices = voices()

    filtered = [voice for voice in my_voices if voice.name == name]

    if len(filtered) == 1:
        return filtered[0]
    else:
        return clone_voice()

def clone_voice():

    if not os.path.exists('audio_clips'):
        create_clips()

    try:
        voice = clone(
            name=name,
            files=glob.glob(f'audio_clips/*.mp3'),
        )
    except:
        my_voices = voices()
        my_voices.voices[-1].delete()
        
        voice = clone(
            name=name,
            files=glob.glob(f'audio_clips/*.mp3'),
        )

    os.rmdir('audio_clips')

    return voice

if __name__ == '__main__':

    voice = get_voice()

    print(voice.name)