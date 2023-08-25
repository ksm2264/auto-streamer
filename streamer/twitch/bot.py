import asyncio
from twitchio.ext import commands
from dotenv import load_dotenv
import os
import time

load_dotenv()

irc_token = os.getenv('TWITCH_IRC_TOKEN')
client_id = os.getenv('TWITCH_CLIENT_ID')
client_secret = os.getenv('TWITCH_CLIENT_SECRET')
nick = 'auto_streamer'
channel = 'auto_streamer'

from streamer.video.command import text_to_video_command, play_video_command

class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(token=irc_token, client_id=client_id, client_secret=client_secret,
                         nick=nick, prefix='!',
                         initial_channels=[channel])

        # as chat messages come in they will be added to this queue
        self.chat_queue = asyncio.Queue()

        # as videos finish processing, commands used to play the vidoe are added to this queue
        self.video_command_queue = asyncio.Queue()

    async def event_ready(self):
        print(f'Ready | {self.nick}')

        # Start the video processing and playback coroutines
        asyncio.create_task(self.process_messages())
        asyncio.create_task(self.play_videos())

    async def event_message(self, message):
        '''
        add message to queue as they come in and print current queue
        '''
        print(message.content)
        await self.chat_queue.put(message.content)
        await self.handle_commands(message)

        print(f'Current message queue: {self.chat_queue}')

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

    async def process_messages(self):
        while True:
            # will wait here until a message arrives from the chat queue 
            message = await self.chat_queue.get()
            
            # for each message, create the video and add the video command to the video queue
            video_command = await text_to_video_command(message)
            await self.video_command_queue.put(video_command)

    async def play_videos(self):
        while True:
            
            # waits here for new video commands
            video_command = await self.video_command_queue.get()

            print('processing new video command')

            # Execute the video command (update OBS 'dynamic' source)
            await play_video_command(video_command)



if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
