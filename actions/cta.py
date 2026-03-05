import ollama
import json

from config.config import MODEL_NAME


def get_cta(code, output, summary):
    response = ollama.chat(
        model=MODEL_NAME,
        format='json',
        messages=[{
            'role': 'user',
            'content': """You have to create a CTA for the text to speech model by judging the ouput and the code, and tell if the task was completed or not.

            Keep it short 3-5 Words.
            Respond in JSON like below.
            {
                "cta": "opened youtube successfully",
            }
            """
            }]
    )
    
    print(json.loads(response['message']['content']))

    return json.loads(response['message']['content'])

