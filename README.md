# auto-streamer

# set up conda env
`conda env create -f env.yaml`

# Set up your accounts and get your keys:
### OpenAI (text to text)
https://platform.openai.com/\
gpt-4 or gpt-3.5-turbo

### Elevenlabs (voice cloning text to audio)
https://elevenlabs.io/\
Voice clone from a few audio samples

### Replicate (audio + picture to video w/ wav2lip)
https://replicate.com/\
Replicate hosts miscellaneous open source models\
note: could potentially run wav2lip locally

### Twitch TV stream and dev account
https://twitchapps.com/tmi/ (TWITCH_IRC_TOKEN)
- Click connect

https://dev.twitch.tv/ (TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
- Your Console -> Applications -> Register Your Application -> `http://localhost` for OAuth Redirect URLS 
- Applications -> Manage -> copy Client ID, and generate Client Secret


https://dashboard.twitch.tv/ (TWITCH_STREAM_KEY)
- Click profile icon -> Creator Dashboard -> Settings -> Stream
- Copy Primary Stream Key

### populate a .env file with these:
```
OPENAI_API_KEY=''
ELEVENLABS_API_KEY=''
REPLICATE_API_TOKEN=''

CHARACTER_NAME='this will be used to prompt gpt and also will be the name of the elevenlabs voice'

VOICE_REF_LINK='find a youtube link that has audio samples'

TWITCH_STREAM_KEY=''
TWITCH_CLIENT_ID=''
TWITCH_CLIENT_SECRET=''
TWITCH_IRC_TOKEN=''
``````


## download character portrait:
save it as `portrait.jpg` in the top level

## create idle animation
https://ai.nero.com/face-animation\
worked well (but it cropped it weirdly)
needed to layer in OBS

## set up obs
https://obsproject.com/
- Connect to twitch (Settings -> Stream -> Twitch)
- Create new Source -> name it 'dynamic' -> check "local file", uncheck "looping"
- Create a looping source with looping animation (local file, looping = True)
- Create an Image source with the portrait, put it behind the looping source (in case Nero cropped the image weirdly)
