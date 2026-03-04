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
                "output": "plain text / plain python code to execute in python sandbox, no formating just code. make sure that the code doesn't take user input"
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
    try:
        with open("temp_code", "w") as f:
            f.write(code)
            f.close()

        namespace = {}
        buffer = io.StringIO()
        sys.stdout = buffer

        exec(code, namespace)

        sys.stdout = sys.__stdout__

        return buffer.getvalue()
    except Exception as e:
        print("Error Running code: ", e)
        return ""
