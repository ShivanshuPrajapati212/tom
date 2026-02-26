import asyncio
from perception.file_watcher import start_watching 
from perception.microphone import init_speech_recognition
from perception.combined_input import get_combined_inputs
from config.config import LOOP_INTERVAL


async def cognition_loop():
    asyncio.create_task(start_watching(["/Users/shivanshu/Coding/"]))
    asyncio.create_task(init_speech_recognition())


    while True:
        inputs = get_combined_inputs() 
        
        print(inputs)
        await asyncio.sleep(LOOP_INTERVAL)
