import whisper
import sounddevice as sd
import numpy as np

class Listener:
    def __init__(self, model_name="base", samplerate=16000, silence_threshold=0.05, pause_duration=2.0):
        self.model = whisper.load_model(model_name)
        self.samplerate = samplerate
        self.silence_threshold = silence_threshold
        self.pause_duration = pause_duration

    def listen(self):
        print("Listening... Speak into the microphone.")

        # Record audio until silence is detected
        audio_buffer = []
        silent_chunks = 0
        chunk_duration = 0.2  # Duration of each audio chunk in seconds
        chunk_size = int(self.samplerate * chunk_duration)

        def is_silent(audio_chunk):
            return np.max(np.abs(audio_chunk)) < self.silence_threshold

        with sd.InputStream(samplerate=self.samplerate, channels=1, dtype='float32') as stream:
            while True:
                # Read a chunk of audio data
                audio_chunk = stream.read(chunk_size)[0].flatten()
                audio_buffer.append(audio_chunk)

                # Check if the audio chunk is silent
                if is_silent(audio_chunk):
                    silent_chunks += 1
                else:
                    silent_chunks = 0

                # Stop listening if silence exceeds the pause duration
                if silent_chunks * chunk_duration > self.pause_duration:
                    break

        # Concatenate audio chunks into a single array
        audio_data = np.concatenate(audio_buffer, axis=0)

        print("Transcribing...")
        # Transcribe the audio using Whisper
        result = self.model.transcribe(audio_data, fp16=False)
        print("Transcribed Text:", result["text"])


# Usage example
if __name__ == "__main__":
    listener = Listener(model_name="base")
    listener.listen()
