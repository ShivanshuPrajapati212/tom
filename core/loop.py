import asyncio
from perception.file_watcher import start_watching, get_file_changes
from perception.microphone import init_speech_recognition, get_microphone
from config.config import LOOP_INTERVAL


async def cognition_loop():
    asyncio.create_task(start_watching(["/Users/shivanshu/Coding/"]))
    asyncio.create_task(init_speech_recognition())


    while True:
    
        # Perception
        file_changes = get_file_changes()
        if file_changes != []:
            print(file_changes) 

        microphone_input = get_microphone()
        if microphone_input != "":
            print(microphone_input)
        
        await asyncio.sleep(LOOP_INTERVAL)
