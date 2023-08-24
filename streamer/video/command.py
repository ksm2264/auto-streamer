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

class VideoCommand(BaseModel):

    path:str
    duration:float
    question:str
    answer:str

speaker = Speaker()

async def text_to_video_command(text: str) -> VideoCommand:

    resp = await get_response_async(text)

    audio = speaker.generate_audio(resp)

    video = get_video_for(audio)

    vid_path = f'{uuid.uuid4()}.mp4'

    with open(vid_path, 'wb') as f:
        f.write(video)

    with VideoFileClip(vid_path) as video:
        duration = video.duration
    
    command = VideoCommand(
        path = os.path.abspath(vid_path),
        duration = duration,
        question = text,
        answer = resp
    )

    return command

async def play_video_command(command: VideoCommand):

    print(f'processing command: {command}')

    set_video_source(command.path, looping = False) 

    time.sleep(command.duration + 1)

    os.remove(command.path)


async def main():
    
    command = await text_to_video_command('hello mr sagan')

    print(command)

if __name__ == '__main__':

    asyncio.run(main())