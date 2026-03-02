import json
import ollama

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
Respond in the given JSON format.

{
  "decision_type": "continue_plan/create_plan/create_plan/complete_goal/reflect/idle",
  "reasoning": "File summary step not completed.",
  "next_action": "generate_summary",
  "confidence": 0.86
}"""

    return output


def reason(prompt, working_memory):
    response = ollama.chat(
        model='gemma2:2b',
        format='json',
        messages=[{
            'role': 'user',
            'content':  createStructuredPrompt(prompt, working_memory)  }]
    )
    
    return json.loads(response['message']['content'])
