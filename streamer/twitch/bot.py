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

        self.loop_vid_path = 'C:\\Users\\karl\\projects\\auto-streamer\\test.mp4'

        self.chat_queue = asyncio.Queue()
        self.video_command_queue = asyncio.Queue()

    async def event_ready(self):
        print(f'Ready | {self.nick}')

        # Start the video processing and playback coroutines
        asyncio.create_task(self.process_messages())
        asyncio.create_task(self.play_videos())

    async def event_message(self, message):
        print(message.content)
        await self.chat_queue.put(message.content)
        await self.handle_commands(message)

        print(f'Current message queue: {self.chat_queue}')

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

    async def process_messages(self):
        while True:
            message = await self.chat_queue.get()
            video_command = await text_to_video_command(message)
            await self.video_command_queue.put(video_command)

    async def play_videos(self):
        while True:

            video_command = await self.video_command_queue.get()

            print('processing new video command')
            # Execute the video command
            await play_video_command(video_command)



if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
