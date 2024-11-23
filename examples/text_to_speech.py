import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (optional, like voice and speech rate)
engine.setProperty('rate', 150)  # Speed percent (higher is faster)
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Speak the text
# text = "hello Tan, what are you working on?"
text = "Tan, please answer me"
engine.say(text)

# Wait for the speech to finish
engine.runAndWait()

