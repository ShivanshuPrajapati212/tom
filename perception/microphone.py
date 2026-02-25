import asyncio
import sounddevice as sd
import queue
import vosk
import json

# Load Vosk model
model = vosk.Model("speech-model-en")
q = queue.Queue()

# Callback to put audio chunks into a queue
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

async def transcribe_stream():
    rec = vosk.KaldiRecognizer(model, 16000)
    print("Listening... Press Ctrl+C to stop.")

    while True:
        # Non-blocking check for audio data
        if not q.empty():
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print("Result:", result.get("text", ""))
            else:
                # Partial result while speaking
                partial = json.loads(rec.PartialResult())
                print("Partial:", partial.get("partial", ""), end="\r")
        await asyncio.sleep(0.01)  # tiny async yield

async def main():
    # Start microphone stream
    with sd.RawInputStream(samplerate=16000, blocksize = 8000, dtype='int16',
                           channels=1, callback=audio_callback):
        await transcribe_stream()

if __name__ == "__main__":
    asyncio.run(main())
