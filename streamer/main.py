from dotenv import load_dotenv
load_dotenv()


import os


from streamer.audio.generate import Speaker
from streamer.text.text import get_response
from streamer.video.video import get_video_for
from streamer.video.playback import play_video_bytes


name = os.getenv('CHARACTER_NAME')

if __name__ == '__main__':

    speaker = Speaker()

    print(f'You are talking to {name}, say something:')
    while True:
        text = input('')

        response = get_response(text)

        audio = speaker.generate_audio(response)
        
        video = get_video_for(audio)

        print(response)
        play_video_bytes(video)