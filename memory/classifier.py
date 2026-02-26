import json
import ollama

def classify_transcription_relevance(transcription):
    response = ollama.chat(
        model='gemma2:2b',
        format='json',
        messages=[{
            'role': 'user',
            'content': """Classify this transcription in the given format.
| Situation          | Priority   |
| ------------------ | ---------- |
| Casual talk        | 0.2        |
| Clarification      | 0.4        |
| Task instruction   | 0.8        |
| Critical command   | 0.95       |
| Emotional distress | 0.9        |


Return Example JSON: {"intent": "create_goal", "confidence": 0-1, "priority": 0-1}

Transcription:""" + transcription
        }]
    )
    return json.loads(response['message']['content'])


