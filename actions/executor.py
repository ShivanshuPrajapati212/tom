import json
import ollama


def action(goal, reasoning):
    response = ollama.chat(
        model='qwen3:8b',
        format='json',
        messages=[{
            'role': 'user',
            'content': f"""You have to execute all the steps in the reasoning and achive the goal.
            GOAL: {goal}, REASONING: {reasoning}
            
            Respond like below in JSON.
            {{

            }}
"""
        }]
    )
    
    return json.loads(response['message']['content'])
