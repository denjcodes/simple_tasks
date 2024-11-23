from groq import Groq
import os
import logging

def setup_logger():
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='prompter.log',
                        filemode='w')
    logger = logging.getLogger(__name__)
    return logger

client = Groq(api_key="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")

class Prompter:
    def __init__(self):
        self.system_prompt = """You are a Vision Query Generator, specifically designed to create clear and focused questions for vision models based on user tasks. Your role is to:

1. Accept a task from a user
2. Think step by step, and analyze what visual information would be needed to complete that task. 
3. Generate a precise question that will prompt a vision model to find and describe the relevant elements in an image

When a user provides a task, you should:

First identify what visual elements would be critical for that task
Then generate a question that combines:

1. What specific items/elements to look for
2. What characteristics of these items matter for the task
3. What relationships or context needs to be described

Given a task in the format
Task: <task description>
you should generate a question in the format
Question: <question description>

Example:
Task: I need to clean this table.
Question: What items are on the table that need to be cleaned?
"""

    def prompt(self, task):
        return f"Task: {task}\nQuestion: "
    
    def generate_question(self, task):
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
    

logger = setup_logger()

prompter = Prompter()

tasks = [
         "I need to organize the pantry.", "I need to identify and recycle.",
         "I need to sort my laundry.", "I need to do gardening.",
         "I need to repair my bike.", "I need to prepare my breakfast."
        ]

for task in tasks:
    question = prompter.generate_question(task).split("Question: ")[-1]
    print(question)
    logger.debug(f"Task: {task}\nQuestion: {question}")
    print("\n")