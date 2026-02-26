import asyncio
import mlx_whisper
import numpy as np
import sounddevice as sd
import sys

# --- Configuration ---
MODEL = "mlx-community/whisper-medium-mlx-8bit"
SAMPLE_RATE = 16000
GAIN = 20.0
SILENCE_THRESHOLD = 0.2
SILENCE_DURATION = 0.8
MIN_SPEECH_DURATION = 0.3

HALLUCINATIONS = {
    "Thank you.", "Thanks for watching.", "Please subscribe.",
    "Subtitle by", "you", "Thank you for watching.", "Bye.",
    "Transcription by", "www.zeoranger.co.uk"
}

microphone_input = ""


def get_microphone():
    global microphone_input 
    curr_input = microphone_input
    microphone_input = "" # reset buffer
    if curr_input == "":
        return []
    return [{"input_type": "mic_input", "content":curr_input}]

def apply_gain(chunk: np.ndarray) -> np.ndarray:
    return np.clip(chunk * GAIN, -1.0, 1.0)

def get_rms(chunk: np.ndarray) -> float:
    return float(np.sqrt(np.mean(chunk**2)))

async def transcription_worker(transcription_queue: asyncio.Queue):
    """
    Single worker that processes transcriptions one at a time.
    Prevents concurrent Metal GPU access that caused the abort.
    """
    loop = asyncio.get_event_loop()
    while True:
        audio_buffer = await transcription_queue.get()

        try:
            result = await loop.run_in_executor(
                None,
                lambda buf=audio_buffer: mlx_whisper.transcribe(
                    buf,
                    path_or_hf_repo=MODEL,
                    word_timestamps=False,
                    condition_on_previous_text=False,
                    language="en",
                    temperature=0.0,
                    task="trascribe"
                )
            )
            for segment in result.get("segments", []):
                text = segment.get("text", "").strip()
                if text and text not in HALLUCINATIONS and len(text) > 2:
                    global microphone_input
                    microphone_input += text + " "
                    print(microphone_input)

        except Exception as e:
            print(f"[transcription error] {e}", file=sys.stderr)

        finally:
            transcription_queue.task_done()

async def audio_processor(audio_queue: asyncio.Queue, transcription_queue: asyncio.Queue):
    """Consume mic chunks, detect speech/silence, enqueue for transcription."""
    speech_buffer = np.array([], dtype=np.float32)
    silent_chunks = 0
    speaking = False
    SILENT_CHUNKS_NEEDED = int(SILENCE_DURATION / 0.05)

    while True:
        chunk = await audio_queue.get()
        rms = get_rms(chunk)

        if rms >= SILENCE_THRESHOLD:
            speaking = True
            silent_chunks = 0
            speech_buffer = np.append(speech_buffer, chunk)

        elif speaking:
            silent_chunks += 1
            speech_buffer = np.append(speech_buffer, chunk)

            if silent_chunks >= SILENT_CHUNKS_NEEDED:
                duration = len(speech_buffer) / SAMPLE_RATE
                if duration >= MIN_SPEECH_DURATION:
                    # Enqueue for the single worker — no concurrent GPU calls
                    await transcription_queue.put(speech_buffer.copy())

                speech_buffer = np.array([], dtype=np.float32)
                speaking = False
                silent_chunks = 0

async def init_speech_recognition():
    print(f"--- Loading {MODEL} ---")

    audio_queue: asyncio.Queue = asyncio.Queue()
    transcription_queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        chunk = apply_gain(indata[:, 0].copy())
        loop.call_soon_threadsafe(audio_queue.put_nowait, chunk)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=int(SAMPLE_RATE * 0.05),  # 50ms blocks
    ):
        print(f"Listening... (Threshold: {SILENCE_THRESHOLD}, Gain: {GAIN}x)")

        await asyncio.gather(
            audio_processor(audio_queue, transcription_queue),
            transcription_worker(transcription_queue),  # single GPU worker
        )

if __name__ == "__main__":
    try:
        asyncio.run(init_speech_recognition())
    except KeyboardInterrupt:
        print("\nStopped.")
