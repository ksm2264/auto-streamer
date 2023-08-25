from dotenv import load_dotenv
load_dotenv()
import os

from streamer.twitch.bot import TwitchBot

env_vars = ['OPENAI_API_KEY',
'ELEVENLABS_API_KEY',
'REPLICATE_API_TOKEN',
'CHARACTER_NAME',
'VOICE_REF_LINK',
'TWITCH_STREAM_KEY',
'TWITCH_CLIENT_ID',
'TWITCH_CLIENT_SECRET',
'TWITCH_IRC_TOKEN']

def ensure_requirements():

    # check for necessary .env entries
    for var in env_vars:
        if var not in os.environ.keys():
            raise KeyError(f'{var} is not defined in .env')

    # check for portrait
    if not os.path.exists('portrait.jpg'):
        raise RuntimeError('you did not save a portrait.jpg')
    
    # check for idle_animation
    if not os.path.exists('idle_animation.gif'):
            raise RuntimeError('you did not save an idle_animation.gif')

if __name__ == '__main__':

    ensure_requirements()

    bot = TwitchBot()
    bot.run()