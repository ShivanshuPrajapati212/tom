import json
import ollama


def file_summarizer(input):
    return f"{input.input_type}: {input.path}"

def long_term_summarizer(input):
    response = ollama.chat(
        model='gemma2:2b',
        format='json',
        messages=[{
            'role': 'user',
            'content': """Summarize this transcription in the given format.
            Return Example JSON: {"summary": "...", "category":"user_command"  "importance": 0-1}

Transcription:"""+input
        }]
    )
    return json.loads(response['message']['content'])

