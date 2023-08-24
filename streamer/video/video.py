from dotenv import load_dotenv
load_dotenv()

import os
import requests
import json
import replicate

def download_bytes(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.content  

def get_video_for(audio_bytes: bytes) -> bytes:

    audio_path = 'temp.mp3'

    with open(audio_path, 'wb') as f:
        f.write(audio_bytes)

    vid_url = replicate.run(
        "devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef",
        input={"face": open('portrait.jpg', 'rb'),
            "audio": open(audio_path, 'rb')}
    )
   
    video_bytes = requests.get(vid_url)

    return video_bytes.content


def get_video_for_gooey_sucks(audio_bytes: bytes) -> bytes:

    with open('audio.mp3', 'wb') as audio_file:
        audio_file.write(audio_bytes)

    files = [
        ("input_face", open('portrait.jpg', "rb")),
        ("input_audio", open('audio.mp3', "rb")),
    ]
    payload = {}

    response = requests.post(
        "https://api.gooey.ai/v2/Lipsync/form/",
        headers={
            "Authorization": "Bearer " + os.environ["GOOEY_API_KEY"],
        },
        files=files,
        data={"json": json.dumps(payload)},
    )

    result = response.json()

    video_url = result['output']['output_video']

    video_bytes = download_bytes(video_url)

    try:
        os.remove('audio.mp3')
    except:
        print('failed to delete audio.mp3')

    return video_bytes

if __name__ == '__main__':

    # text = 'sheeeeeeeeeeeeeeeeeeeeeeeeeesh'

    # speaker = Speaker()

    # audio = speaker.generate_audio(text)

    with open('audio.mp3', 'rb') as f:
        audio = f.read()

    video = get_video_for(audio)

    video_path = 'test_5.mp4'

    with open(video_path, 'wb') as f:
        f.write(video)

    # clip = VideoFileClip(video_path)
    # clip.write_videofile(video_path, codec='libx264')
    
