from groq import Groq
import os
import logging

def setup_logger():
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='image_requestor.log',
                        filemode='w')
    logger = logging.getLogger(__name__)
    return logger

client = Groq(api_key="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")

class ImageRequestor:
    def __init__(self):
        self.system_prompt = """You are helpful AI agent. Given a task description, you should request the user to take a picture of the relevant scene.

When a user provides a task, you should generate a request for an image in the format:
Request: <request description>

Example:
Task: I need to clean this table.
Request: Please take a picture of the table.
"""

    def prompt(self, task):
        return f"Task: {task}\nRequest: "
    
    def generate_request(self, task):
        completion = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": self.prompt(task)}
                        ],
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        stream=False,
                        stop=None,
                    )
        return completion.choices[0].message.content
    

if __name__ == "__main__":
    logger = setup_logger()
    image_requestor = ImageRequestor()
    
    tasks = [
            "I need to organize the pantry.", "I need to identify and recycle.",
            "I need to sort my laundry.", "I need to do gardening.",
            "I need to repair my bike.", "I need to prepare my breakfast."
            ]

    for task in tasks:
        logger.info(f"Generating request for task: {task}")
        request = image_requestor.generate_request(task).split("Request: ")[-1]
        logger.info(f"Generated request: {request}")
        print(request)