import whisper, numpy, ffmpeg

# Load the Whisper model
model = whisper.load_model("base")

# Transcribe audio from a file
result = model.transcribe("/Users/dj/Documents/GitHub/simple_tasks/examples/test.wav")
print("Transcribed Text:", result["text"])
