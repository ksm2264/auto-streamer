import obswebsocket
from obswebsocket import requests
import keyboard
import time

host = "localhost"
port = 4444
password = "123"  # If you have set a password for obs-websocket in OBS
scene_name = 'Scene'

def set_video_source(vid_path: str, looping = False):
    client = obswebsocket.obsws(host, port, password)
    client.connect()
    client.call(requests.SetSourceSettings( sourceName='dynamic', sourceSettings ={"local_file":vid_path, "looping": looping}))
    client.disconnect()

if __name__ == "__main__":
    looping_file_path = 'C:\\Users\\karl\\projects\\auto-streamer\\test_1.mp4'
    other_vid_path = 'C:\\Users\\karl\\projects\\auto-streamer\\test_2.mp4'

    toggle = False

    while True:
        if keyboard.is_pressed('s'):
            print('switching')
            time.sleep(1)  # To debounce the key press and prevent rapid switching
            if toggle:
                # Switch to the looping video in OBS using the OBS Websocket API
                set_video_source(looping_file_path)
                toggle = False
            else:
                # Switch to the non-looping video
                set_video_source(other_vid_path)
                toggle = True