import os
from dotenv import load_dotenv
load_dotenv()

from elevenlabs import play


from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from streamer.audio.generate import Speaker

name = os.getenv('CHARACTER_NAME')

TEMPLATE = '''
You are {name}

Respond like them to the next question / statement.
:
{message}
'''

prompt = PromptTemplate(input_variables = ['name', 'message'],
                          template = TEMPLATE)


llm = ChatOpenAI(
    model_name='gpt-4'
)

chain = LLMChain(
    llm = llm,
    prompt = prompt,
    verbose = True
)


def get_response(text: str):

    response = chain.predict(name=name,
                    message=text)
    
    return response

if __name__ == '__main__':

    speaker = Speaker()

    print(f'You are talking to {name}, say something:')
    while True:
        text = input('')

        response = get_response(text)
        
        audio = speaker.generate_audio(response)
        
        print(response)
        play(audio)