import asyncio 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

paths_to_watch = [
        "/Users/shivanshu/Documents/",
        "/Users/shivanshu/Desktop/",
        "/Users/shivanshu/Coding/",
]

file_changes = []

class BufferedHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            # store change in buffer
            file_changes.append({
                "input_type": f"file_{event.event_type}",
                "path": event.src_path
            })


async def start_watching(paths=paths_to_watch):
    loop = asyncio.get_event_loop()
    observer = Observer()
    handler = BufferedHandler()
    
    for path in paths:
        observer.schedule(handler, path, recursive=True)

    # Start the observer in a separate thread
    observer.start()

    try:
        while True:
            await asyncio.sleep(1)  # keep the loop alive
    except asyncio.CancelledError:
        observer.stop()
        observer.join()


# Function to get all buffered changes since last call
def get_file_changes():
    global file_changes
    changes = file_changes.copy()
    file_changes.clear()  # reset buffer
    return changes


# Example usage
async def example():
    # Start watcher asynchronously
    watcher_task = asyncio.create_task(start_watching(paths_to_watch))

    try:
        while True:
            await asyncio.sleep(5)  # check every 5 seconds
            changes = get_file_changes()
            if changes:
                print("New changes since last check:")
                for c in changes:
                    print(f"{c['input_type'].upper()}: {c['path']}")
    except KeyboardInterrupt:
        watcher_task.cancel()
        await watcher_task


if __name__ == "__main__":
    asyncio.run(example())
