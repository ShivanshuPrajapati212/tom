import json
import ollama

def classify_relevance(transcription):
    response = ollama.chat(
        model='gemma2:2b',
        format='json',
        messages=[{
            'role': 'user',
            'content': """Classify this transcription in the given format.
Return Example JSON: {"intent": "create_goal", "confidence": 0-1, "priority": 0-1}

Transcription:""" + transcription
        }]
    )
    return json.loads(response['message']['content'])

