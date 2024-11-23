import groq

client = groq.Groq(api_key="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")

class TaskBreaker:
    def __init__(self):
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

    def initial_prompt(self, task, query, description):
        return f"""Task: {task}
                    Query: {query}
                    Description: {description}
                    Steps:
                """
    
    def init_messages(self, task, query, description):
        return [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.initial_prompt(task, query, description)}
                ]
    
    def generate_steps(self, task, query, description):
        i = 0
        while i < 5:
            completion = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=self.init_messages(task, query, description),
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
                
        #     steps = completion.choices[0].message.content.split("\n")[6:]
        #     if len(steps) > 1:
        #         return steps
        #     i += 1
        # completion = client.chat.completions.create(
        #                 model="llama-3.1-70b-versatile",
        #                 messages=self.init_messages(task, query, description),
        #                 temperature=1,
        #                 max_tokens=1024,
        #                 top_p=1,
        #                 stream=False,
        #                 stop=None,
        #             )
        # return completion.choices[0].message.content
    def breakdown_steps(self, task, query, description, steps):
        return {
            "task": task,
            "query": query,
            "description": description,
            "steps": steps,
            "current_step": 0,
            "scene_description": None
        }

    def update_task(self, memory, scene_description=None):
        if scene_description:
            memory["scene_description"] = scene_description
        
        current_step = memory["current_step"]
        if current_step < len(memory["steps"]):
            next_step = memory["steps"][current_step]
            return {
                "status": "in progress",
                "next_step": next_step,
                "on_track": True  # Add logic to determine if the scene aligns with the steps
            }
        else:
            return {"status": "complete", "next_step": None, "on_track": True}

    def complete_step(self, memory):
        if memory["current_step"] < len(memory["steps"]):
            memory["current_step"] += 1

    
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
    
    for task, query, description in zip(tasks, queries, descriptions):
        memory = task_breaker.generate_steps(task, query, description)
        steps = task_breaker.breakdown_steps(task, query, description, memory)

        print("Initial Task Breakdown:", steps)

        while True:
            # User interaction for current step
            step_info = task_breaker.update_task(steps)
            if step_info["status"] == "complete":
                print("Assistant: Great! The task is complete.")
                break

            print(f"Assistant: The next step is: {step_info['next_step']}")
            
            # User input
            user_input = input("Has this step been completed? (Y/N): ").strip().lower()
            if user_input == "y":
                task_breaker.complete_step(steps)
            else:
                print("Assistant: Let me know when it's done.")
        break

