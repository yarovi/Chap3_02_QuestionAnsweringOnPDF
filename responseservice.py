from openai import OpenAI

from config import Settings

client = OpenAI()

class ResponseService():
    def __init__(self):
        pass

    def generate_response(self, facts, user_question):
        response = client.chat.completions.create(model=Settings.MODEL_CHAT,
                                                  messages=[
                                                      {"role": "user", "content": 'Based on the FACTS, give an answer to the QUESTION. '+
                                                                                  f'QUESTION: {user_question}. FACTS: {facts}'}
                                                  ])

        # extract the response
        return (response.choices[0].message.content)