import mlx_whisper
import numpy as np
import sounddevice as sd
import queue

# Settings
MODEL = "mlx-community/whisper-large-v3-turbo"
SAMPLE_RATE = 16000
CHUNK_DURATION = 1  # Seconds of audio to process at a time
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called by sounddevice for every audio block"""
    if status:
        print(status)
    audio_queue.put(indata.copy())

def stream_transcribe():
    print(f"--- Loading {MODEL} onto M4 GPU ---")
    
    # Start microphone stream
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback):
        print("Listening... (Press Ctrl+C to stop)\n")
        
        audio_buffer = np.array([], dtype=np.float32)
        
        try:
            while True:
                # Get audio from queue
                while not audio_queue.empty():
                    data = audio_queue.get()
                    audio_buffer = np.append(audio_buffer, data)

                # Process if we have enough audio for a chunk
                if len(audio_buffer) > SAMPLE_RATE * CHUNK_DURATION:
                    # MLX Whisper transcribes the buffer
                    result = mlx_whisper.transcribe(
                        audio_buffer, 
                        path_or_hf_repo=MODEL,
                        fp16=True # Uses M4's FP16 acceleration
                    )
                    
                    print(f"Transcript: {result['text'].strip()}")
                    
                    # Clear buffer to start fresh for the next chunk
                    # Or keep a small overlap for better context
                    audio_buffer = np.array([], dtype=np.float32)
                    
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    stream_transcribe()
