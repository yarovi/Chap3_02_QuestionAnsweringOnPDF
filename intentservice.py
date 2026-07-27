from openai import OpenAI

from config import Settings

client = OpenAI()

class IntentService:
    def __init__(self):
        pass

    def get_intent(self, user_question: str):
        # call the openai ChatCompletion endpoint
        response = client.chat.completions.create(model=Settings.MODEL_CHAT,
                                                  messages=[
                                                      {"role": "user",
                                                       "content": f'Extract the keywords from the following question: {user_question}' +
                                                                  'Do not answer anything else, only the keywords.'}
                                                  ])

        # extract the response
        return (response.choices[0].message.content)