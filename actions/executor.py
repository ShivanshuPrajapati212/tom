import json
import re
import ollama
import io
import sys

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


    output = json.loads(response['message']['content'])

    if output["type"]  == "code":
        res = run_code(output["output"])
        return "Code Result: " + res 
    if output["output"] == "plain":
        return output["output"]
    
    return 
def run_code(code):
    namespace = {}
    buffer = io.StringIO()
    sys.stdout = buffer

    exec(code, namespace)

    sys.stdout = sys.__stdout__

    return buffer.getvalue()
