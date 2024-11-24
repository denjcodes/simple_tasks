from groq import Groq
import os
import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='logs/image_question_generator.log',
                        filemode='w')
    logger = logging.getLogger(__name__)
    return logger

client = Groq(api_key="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")

class ImageQuestionGenerator:
    def __init__(self):
        self.system_prompt = """
You are a Vision Query Generator. Given a user defined task:

Your job is to question what the user sees. You care about:
1. The high level description of the image.
2. The objects inside the image.
3. Unique adjective for each object.
4. Location of each object.

Create a clear and concise question that highlights what to look for and understand the environment. 
Remember if there are no noticable objects, its best to not hallucinate them.
Input:
Task: <task description>

Output:
Question: <question description>

Example:
Task: I need to make breakfast.
Question: Where are you and food items do you see? Are any of them expired? Where do you see them?
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

if __name__ == "__main__":
    logger = setup_logger()

    image_question_generator = ImageQuestionGenerator()

    tasks = [
            "I need to organize the pantry.", "I need to identify and recycle.",
            "I need to sort my laundry.", "I need to do gardening.",
            "I need to repair my bike.", "I need to prepare my breakfast."
            # "I want to clean this table."
            ]

    for task in tasks:
        question = image_question_generator.generate_question(task).split("Question: ")[-1]
        print(question)
        logger.info(f"Task: {task}\nQuestion: {question}")
        print("\n")