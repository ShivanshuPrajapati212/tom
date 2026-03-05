import ollama
import json


def get_cta(code, output, summary):
    response = ollama.chat(
            model="gemma3:4b",
        format='json',
        messages=[{
            'role': 'user',
            'content': """You have to summary the output by judging the ouput and the code.

            Keep it short 3-5 Words.
            Respond in JSON like below.

            Example:
            {
                "cta": "Eg: the current time is 8:30pm",
            }
            """
            }]
    )
    
    print(json.loads(response['message']['content']))

    return json.loads(response['message']['content'])

if __name__ == "__main__":
    get_cta("import subprocess; subprocess.run(['open', '-a', 'Finder'])", None, "User requested to Open finder")
