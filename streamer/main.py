from dotenv import load_dotenv
load_dotenv
import os

from streamer.twitch.bot import TwitchBot

def ensure_requirements():

    # check for necessary .env entries

    # check for portrait

    # check for idle_animation

    # ensure elevenlabs has voice, otherwise create it
    pass


if __name__ == '__main__':

    ensure_requirements()

    bot = TwitchBot()
    bot.run()