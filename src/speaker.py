import pyttsx3

class TextToSpeech:
    def __init__(self, rate=150, volume=0.9):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)


# Usage Example
if __name__ == "__main__":
    tts = TextToSpeech(rate=150, volume=0.9)
    tts.speak("Faiz, Sharuka, are you guys hungry?")
