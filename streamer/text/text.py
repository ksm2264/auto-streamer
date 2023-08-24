import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


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
    model_name='gpt-3.5-turbo'
)

chain = LLMChain(
    llm = llm,
    prompt = prompt,
    verbose = True
)

async def get_response_async(text: str) -> str:

    response = await chain.apredict(name=name,
                    message=text)
    
    return response

def get_response(text: str):

    response = chain.predict(name=name,
                    message=text)
    
    return response

async def main():
 # speaker = Speaker()

    print(f'You are talking to {name}, say something:')
    while True:
        text = input('')

        response = await get_response_async(text)
        
        print(response)


if __name__ == '__main__':
    asyncio.run(main())
   