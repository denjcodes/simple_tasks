from speaker import TextToSpeech
from listener import Listener

tts = TextToSpeech()
stt = Listener()

tts.speak("Hello, How can I help you?")
while True:
    task = None
    while task is None:
        task = stt.listen()
    tts.speak("Did you say " + task + "?")
    while True:
        confirm = stt.listen()
        if "yes" in confirm.lower():
            tts.speak("Great!")
            break
        elif "no" in confirm.lower():
            tts.speak("I'm sorry. Please try again.")
            break
        else:
            tts.speak("I'm sorry. I didn't understand that.")
    if "yes" in confirm.lower():
        break
    if "no" in confirm.lower():
        continue

from image_requestor import ImageRequestor
image_requestor = ImageRequestor()

image_request = image_requestor.generate_request(task).split("Request: ")[-1]
tts.speak(image_request)

from image_question_generator import ImageQuestionGenerator
image_question_generator = ImageQuestionGenerator()
image_question = image_question_generator.generate_question(task).split("Question: ")[-1]

# Wait for the image to be captured
