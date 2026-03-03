import json
import ollama

from config.config import MODEL_NAME
 

def action(goal, reasoning):
    response = ollama.chat(
        model=MODEL_NAME,
        format='json',
        messages=[{
            'role': 'user',
            'content': f"""You have to execute all the steps in the reasoning and achive the goal.
            GOAL: {goal}, REASONING: {reasoning}
            
            Respond like below in JSON.
            {{
                "type": "plain" or "code",
                "output": "plain text / code to execute in python sandbox"
            }}"""
        }]
    )
    
    return json.loads(response['message']['content'])
