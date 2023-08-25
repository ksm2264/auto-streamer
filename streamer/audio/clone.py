from elevenlabs import clone, set_api_key, voices, Voice
import os
import glob
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('ELEVENLABS_API_KEY')
set_api_key(api_key)

name = os.getenv('CHARACTER_NAME')

from streamer.audio.clip import create_clips

def get_voice() -> Voice:
    my_voices = voices()

    filtered = [voice for voice in my_voices if voice.name == name]

    # return voice with name if found, otherwise create it
    if len(filtered) == 1:
        return filtered[0]
    else:
        return clone_voice()

def clone_voice() -> Voice:

    # if audio clips don't exist yet, create them from youtube video linked in .env
    if not os.path.exists('audio_clips'):
        create_clips()

    # elevenlabs account has stored voices limit, delete one and then close if that's the case
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