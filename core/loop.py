import asyncio
from cognition.reason import reason
from memory import short_term, update_memory
from memory.sqlite import get_all_rows
from perception.file_watcher import start_watching 
from perception.microphone import init_speech_recognition
from perception.combined_input import get_combined_inputs
from config.config import LOOP_INTERVAL


async def cognition_loop():
    asyncio.create_task(start_watching(["/Users/shivanshu/Coding/"]))
    asyncio.create_task(init_speech_recognition())


    while True:
        inputs = get_combined_inputs() 
        print("Inputs: ", inputs)
        summary = update_memory.update_memory(inputs)
        print("Short Term: ", short_term.working_memory["recent_events"])
        print("Long Term: ", get_all_rows()) 
        if summary == "":
            await asyncio.sleep(LOOP_INTERVAL)
            continue

        reasoning = reason(summary, short_term.working_memory)
        print(reasoning)

        await asyncio.sleep(LOOP_INTERVAL)
