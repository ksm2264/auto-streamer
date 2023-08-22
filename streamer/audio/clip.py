import os
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import AudioFileClip

from dotenv import load_dotenv
load_dotenv()

TEMP_CLIPS_PATH = 'audio_clips'

def download_youtube_video():

    vid_url = os.getenv('VOICE_REF_LINK')

    yt = YouTube(vid_url)
    stream = yt.streams.first()
    stream.download()

    return stream.default_filename

def cut_into_clips(vid_path: str, clip_length=12):

    if not os.path.exists(TEMP_CLIPS_PATH):
        os.mkdir(TEMP_CLIPS_PATH)

    try:
        start_time = 0
        end_time = clip_length
        clip_index = 0

        while end_time <= 120:  # 2 minutes in seconds
            target_file = os.path.join(TEMP_CLIPS_PATH, f'clip_{clip_index}.mp4')
            ffmpeg_extract_subclip(vid_path, start_time, end_time, targetname=target_file)

            # Convert the clip to mp3
            audioclip = AudioFileClip(target_file)
            audioclip.write_audiofile(os.path.join(TEMP_CLIPS_PATH, f'clip_{clip_index}.mp3'))

            clip_index += 1
            start_time = end_time
            end_time += clip_length

    except Exception as e:
        print(e)

def create_clips():
    video_file = download_youtube_video()
    cut_into_clips(video_file)
    os.remove(video_file)


if __name__ == "__main__":
   create_clips()
