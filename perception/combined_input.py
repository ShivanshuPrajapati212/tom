from perception.file_watcher import get_file_changes
from perception.microphone import get_microphone

def get_combined_inputs():
    file_inputs = get_file_changes()
    mic_input = get_microphone()

    return file_inputs + mic_input 

