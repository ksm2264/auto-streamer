import io
import vlc
import time

def play_video_bytes(video_bytes):
    # Create a named temporary file
    with io.BytesIO(video_bytes) as f:
        with open("temp_video.mp4", "wb") as out_file:
            out_file.write(f.read())

    # Create an instance of the VLC player
    instance = vlc.Instance()
    player = instance.media_player_new()

    # Set the media for the player
    media = instance.media_new("temp_video.mp4")
    player.set_media(media)

    # Play the video
    player.play()

    # Keep the script running while video is playing
    time.sleep(1)
    while player.is_playing():
        time.sleep(0.1)

    # Stop the player and release resources
    player.stop()
    player.release()

if __name__ == '__main__':

    with open("test.mp4", "rb") as f:
        video_bytes = f.read()

    play_video_bytes(video_bytes)