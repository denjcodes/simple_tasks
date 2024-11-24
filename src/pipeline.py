from speaker import TextToSpeech
from listener import Listener
import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='logs/pipeline.log',
                        filemode='w')
    logger = logging.getLogger(__name__)
    return logger
logger = setup_logger()

tts = TextToSpeech()
stt = Listener()

tts.speak("Hello, How can I help you?")
while True:
    task = None
    while task is None:
        task = stt.listen()
    tts.speak("Did you say " + task + "?")
    logger.info(f"Heard Task: {task}")
    while True:
        confirm = stt.listen()
        logger.info(f"Heard Confirmation: {confirm}")
        if "yes" in confirm.lower():
            tts.speak("Great!")
            logger.info("Task confirmed.")
            break
        elif "no" in confirm.lower():
            tts.speak("I'm sorry. Please try again.")
            logger.info("Task not confirmed. Asking again.")
            break
        else:
            tts.speak("I'm sorry. I didn't understand that.")
            logger.info("Heard an invalid response. Asking again.")
    if "yes" in confirm.lower():
        break
    if "no" in confirm.lower():
        continue

from image_requestor import ImageRequestor
image_requestor = ImageRequestor()
image_request = image_requestor.generate_request(task).split("Request: ")[-1]
tts.speak(image_request)
logger.info(f"Generated Image Request: {image_request}")

from image_question_generator import ImageQuestionGenerator
image_question_generator = ImageQuestionGenerator()
image_question = image_question_generator.generate_question(task).split("Question: ")[-1]
logger.info(f"Generated Image Question: {image_question}")

image_path = 'images/can_jelly_bottle.jpg'
from image_describer import ImageDescriber
image_describer = ImageDescriber()
description = image_describer.generate_description(image_question, image_path).split("Description: ")[-1]
logger.info(f"Generated Image Description: {description}")

from task_breaker import TaskBreaker
task_breaker = TaskBreaker(task=task, image_query=image_question, description=description)
task_breaker.guide_through_task()
