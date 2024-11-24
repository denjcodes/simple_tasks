import groq
from image_describer import ImageDescriber
import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='logs/task_breaker.log',
                        filemode='w')
    logger = logging.getLogger(__name__)
    return logger
logger = setup_logger()

client = groq.Groq(api_key="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")
image_describer = ImageDescriber()

class TaskBreaker:
    def __init__(self, task=None, image_query=None, description=None):
        self.system_prompt = """You are a supportive assistant specialized in breaking down tasks for people with cognitive differences like ADHD and Down Syndrome. When given:

                                A high-level task objective
                                A vision query about an image
                                A description of that image

                                You will:

                                Break the task into small, clear steps
                                Use simple, direct language
                                Mention specific items/locations from the image
                                Provide encouraging feedback between steps
                                Provide a complete plan to help the user complete the task

                                Keep steps short and visual. Focus on "what I see" and "what I do." If a step seems complex, break it down further. Be patient and supportive in your tone.

                                Given a task, a query, and a description, you should generate a series of steps in a python list format.
                                Task: <task description>
                                Query: <query description>
                                Description: <description>
                                Steps:
                                ["1. <step 1>", 
                                "2. <step 2>", 
                                "3. <step 3>",
                                ...]

                                Example:
                                Task: Organize the pantry.
                                Query: What types of food items and containers are present in the pantry, and how are they currently arranged on the shelves?
                                Description: The pantry has 3 shelves. There is a sugar container on the top shelf, a bread loaf and some containers. The middle shelf has some pots and potatoes. The bottom shelf has some cans, apples and empty jars.
                                Steps:
                                ["1. Take out the bread loaf and the sugar container.",
                                "2. Take out the jars and apples from the bottom shelf.",
                                "3. Move the pots to the top shelf.",
                                "4. Move the potates to the bottom shelf.",
                                "5. Place the sugar container on the left side of the middle shelf.",
                                "6. Place the bread loaf next to the sugar container.",
                                "7. Put the jars on the right side of the top shelf.",
                                "8. Put the apples on the right side of the middle shelf."]
                            """
        self.messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.initial_prompt(task, image_query, description)}
                ]
        self.status = {
            "task": task,
            "image_query": image_query,
            "initial_screen_description": description,
            "plan": self.generate_plan(),
            "steps_history": [],
            "current_screen_description": None,
        }

    def initial_prompt(self, task, query, description):
        return f"""Task: {task}
                    Query: {query}
                    Description: {description}
                    Steps:
"""
    
    def generate_plan(self):
        i = 0
        while i < 5:
            completion = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=self.messages,
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        stream=False,
                        stop=None,
                    )
            if "Steps:" not in completion.choices[0].message.content:
                print(f'"Steps:" not found in completion. Attempt {i}')
                i += 1
                continue
            steps = completion.choices[0].message.content.split("Steps:")[-1]
            try:
                steps = eval(steps)
                return steps
            except:
                print(f"Output not in list format. Attempt {i}")
                i += 1

    def guide_system_prompt(self):
        return f"""You are a supportive assistant specialized in breaking down tasks for people with cognitive differences like ADHD and Down Syndrome.
Given the Task, Image Query, Answer to the Image Query, and the Plan, you will guide the user through the task by providing clear, concise instructions and encouraging feedback.
The user will update you with the current scene description after each step, and you will determine if the user is on track to complete the task.
Your task is to guide the user through the task by providing clear, concise instructions to perform the next step and encouraging feedback."""

    def guide_user_prompt(self):
        step_history = ""
        for i, step in enumerate(self.status["steps_history"]):
            step_history += f"{i+1}. {step}\n"

        return f"""# Task:\n{self.status["task"]}
# Image Query:\n{self.status["image_query"]}
# Description:\n{self.status["initial_screen_description"]}
# Plan:\n{"\n".join(self.status["plan"])}
# Steps History:\n{step_history}
# Current Screen Description:\n{self.status["current_screen_description"]}

What should I do next?
# Next Step:
"""

    def guide_through_task(self):
        while True:
            next_step = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=[
                            {"role": "system", "content": self.guide_system_prompt()},
                            {"role": "user", "content": self.guide_user_prompt()}
                        ],
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        stream=False,
                        stop=None,
                    ).choices[0].message.content.split("# Next Step:")[-1].strip()
            self.log_status()
            print(f"Next Step: {next_step}")
            logger.info(f"Next Step: {next_step}")
            self.status["steps_history"].append(next_step)
            new_image_path = input("Please provide the path to the new image: ")
            if new_image_path == "exit":
                break
            self.update_screen_description(new_image_path)
    
    def update_screen_description(self, new_image_path):
        self.status["current_screen_description"] = image_describer.generate_description(self.status["image_query"], new_image_path).split("Description: ")[-1]

    def log_status(self):
        logger.info(f"Task: {self.status['task']}\nImage Query: {self.status['image_query']}\nInitial Screen Description: {self.status['initial_screen_description']}\nPlan: {self.status['plan']}\nSteps History: {self.status['steps_history']}\nCurrent Screen Description: {self.status['current_screen_description']}")
    
if __name__ == "__main__":
    task_breaker = TaskBreaker()
    
    tasks = [
            # "Organize the pantry.", "Identify and recycle.",
            # "Sort my laundry.", "Do gardening.",
            # "Repair my bike.", "Prepare my breakfast."
            "I want to clean this table."
            ]
    
    queries = [
            # "What types of food items and containers are present in the pantry, and how are they currently arranged on the shelves?",
            # "What objects in the scene are made of paper, plastic, glass, or metal, and how are they currently disposed of (e.g., in trash or recycling bins)?",
            # "What types of clothing, including their dominant colors and fabric care labels, are visible in the laundry pile?",
            # "What plants and weeds are in the gardening area, and what is their condition - e.g., are they healthy, dry, or overgrown?",
            # "What components of the bicycle (such as wheels, brakes, gears, or chain) appear damaged or worn out, and what tools or spare parts might be needed to repair them in the surrounding workspace or storage area?",
            # "What edible items, such as fruits, bread, eggs, or breakfast cereals, are visible on the countertops or in the open cabinets in the kitchen?",
            "What objects are on the table, and what is their condition in terms of dirtiness or clutter, to guide the cleaning process?"
            ]
    
    descriptions = [
            # "The pantry is full of food items and containers. They are arranged on the shelves by category.",
            # "There are objects made of paper, plastic, glass, and metal. They are disposed of in separate trash and recycling bins.",
            # "The laundry pile contains various types of clothing. Each item has a fabric care label with washing instructions.",
            # "The gardening area has a mix of plants and weeds. Some are healthy, while others look dry or overgrown.",
            # "The bicycle has several damaged components like wheels, brakes, and gears. Repair tools and spare parts are scattered around.",
            # "The kitchen countertops and cabinets have fruits, bread, eggs, and breakfast cereals on display.",
            "The table features two water bottles, one with a label indicating it is half full and the other with a label indicating it is nearly empty. Additionally, there are two cans, one of which appears to be empty and the other with a label indicating it is nearly full. A bag of chips is also present, with some of its contents spilled out onto the table. The overall condition of the table is moderately dirty, with visible crumbs and spills from the chips."            
            ]
    
    task_breaker.guide_through_task(tasks, queries, descriptions)

