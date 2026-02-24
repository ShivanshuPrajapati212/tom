import asyncio
from perception.file_watcher import start_watching, get_file_changes
from config.config import LOOP_INTERVAL


async def cognition_loop():
    asyncio.create_task(start_watching(["/Users/shivanshu/Coding/"]))

    while True:
        file_changes = get_file_changes()
        if file_changes == []:
            await asyncio.sleep(LOOP_INTERVAL)
            continue
        
        print(file_changes) 
        await asyncio.sleep(LOOP_INTERVAL)
