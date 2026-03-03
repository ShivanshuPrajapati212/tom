import json
import ollama
from config.config import MODEL_NAME

def createStructuredPrompt(prompt, working_memory):
    output = "CURRENT GOAL:\n"
    output += prompt + "\n"
    output += "PLAN STATUS:\n"
    for step in working_memory["current_plan"]["steps"]:
        if step["status"] == "completed":
            output += "- completed: " + step["content"] + "\n"
        if step["status"] == "pending":
            output += "- pending: " + step["content"] + "\n"

    if len(working_memory["current_plan"]["steps"]) == 0:
        output += "No Steps/Plan Found.\n"

    output += "RECENT EVENTS:\n"
    for event in working_memory["recent_events"]:
        output +=  "- " + event + "\n"

    output += """QUESTION:
What should be the next structured action?
Give step by step plan to accomplise the goal.
Respond in the given JSON format.

{
  "decision_type": "generate_summary",
  "reasoning": "File summary step completed.",
  "steps": ["Read the document", "Generate Summary"],
  "confidence": 0.86
}"""

    return output


def reason(prompt, working_memory):
    response = ollama.chat(
        model=MODEL_NAME,
        format='json',
        messages=[{
            'role': 'user',
            'content':  createStructuredPrompt(prompt, working_memory)  }]
    )
    
    return json.loads(response['message']['content'])
