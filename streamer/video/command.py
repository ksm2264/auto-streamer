from pydantic import BaseModel
import asyncio
import uuid
from moviepy.editor import VideoFileClip
import time
import os

from streamer.text.text import get_response_async
from streamer.audio.generate import Speaker
from streamer.video.video import get_video_for
from streamer.twitch.obs import set_video_source

# encapsulate information needed to play video
class VideoCommand(BaseModel):

    path:str
    duration:float
    question:str
    answer:str

# takes a while to spool up so we persist an instance here
speaker = Speaker()

async def text_to_video_command(text: str) -> VideoCommand:

    # gpt answers the question
    resp = await get_response_async(text)

    # elevenlabs generates audio from the text
    audio = speaker.generate_audio(resp)

    # wav2lip generates the video from the audio + portrait.jpg
    video = get_video_for(audio)

    # write the video bytes as a video file for OBS to play easily
    vid_path = f'{uuid.uuid4()}.mp4'

    with open(vid_path, 'wb') as f:
        f.write(video)

    with VideoFileClip(vid_path) as video:
        duration = video.duration
    
    # create video command which can be used later to pass relevant info to OBS
    command = VideoCommand(
        path = os.path.abspath(vid_path),
        duration = duration,
        question = text,
        answer = resp
    )

    return command

async def play_video_command(command: VideoCommand):

    print(f'processing command: {command}')

    # tell OBS to play particular video
    set_video_source(command.path, looping = False) 

    # wait for the duration of the video, and then one more second
    time.sleep(command.duration + 1)

    # delete the video (so we don't persist all of the videos on disk)
    os.remove(command.path)


async def main():
    
    command = await text_to_video_command('hello mr sagan')

    print(command)

if __name__ == '__main__':

    asyncio.run(main())