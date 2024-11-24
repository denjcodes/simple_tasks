from groq import Groq
import os
import logging
import base64
import subprocess
import os

def setup_logger():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='logs/image_describer.log',
                        filemode='w')
    logger = logging.getLogger(__name__)
    return logger

client = Groq(api_key="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")

class ImageDescriber:
    def __init__(self):
        self.system_prompt = None

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def prompt(self, question):
        return f"""You are a Image Analyzer, specifically designed to create clear and focused descriptions for images based on user questions. Your role is to:

1. Accept a question from a user
2. Analyze the image to find relevant elements
3. Generate a precise description that answers the user's question

When a user provides a question, you should:
First analyze the image to find the relevant elements
Then generate a description that combines:

1. What specific items/elements from the user's question are in the image
2. What characteristics of these items matter for the question
3. What relationships or context needs to be described

Given a question in the format
Question: <question description>
you should generate a description in the format
Description: <description>

Generate a description for the following question:
Question: {question}
Description:"""
        # return f"Question: {question}\nDescription: "
    
    def generate_description(self, question, image_path):
        completion = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[
                            # {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": [
                                {"type": "text", "text": self.prompt(question)},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.encode_image(image_path)}"}}
                            ]}
                        ],
                        temperature=0.2,
                        max_tokens=1024,
                        top_p=1,
                        stream=False,
                        stop=None,
                    )
        return completion.choices[0].message.content
    
    def update_picture(self):
        # Define the Node.js script and expected output file
        node_script = "src/capture.js"
        output_file = os.path.join("images", "test_photo.jpg")

        try:
            # Run the Node.js script
            # print("Running Node.js script to capture image...")
            # subprocess.run(["node", node_script], check=True)
            subprocess.run(["node", node_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # Verify if the image file was created
            if os.path.exists(output_file):
                print(f"Image captured successfully: {output_file}")
                image_paths = [output_file]  # Store in a Python list
                print("Image paths:", image_paths)
            else:
                print(f"Error: Output file {output_file} not found.")

        except subprocess.CalledProcessError as e:
            print(f"Error while running Node.js script: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    logger = setup_logger()
    image_describer = ImageDescriber()
    
    questions = [
            # "What types of food items and containers are present in the pantry, and how are they currently arranged on the shelves?",
            # "What objects in the scene are made of paper, plastic, glass, or metal, and how are they currently disposed of (e.g., in trash or recycling bins)?",
            # "What types of clothing, including their dominant colors and fabric care labels, are visible in the laundry pile?",
            # "What plants and weeds are in the gardening area, and what is their condition - e.g., are they healthy, dry, or overgrown?",
            # "What components of the bicycle (such as wheels, brakes, gears, or chain) appear damaged or worn out, and what tools or spare parts might be needed to repair them in the surrounding workspace or storage area?",
            # "What edible items, such as fruits, bread, eggs, or breakfast cereals, are visible on the countertops or in the open cabinets in the kitchen?",
            "What objects are on the table, and what is their condition in terms of dirtiness or clutter, to guide the cleaning process?"
            ]
    

    image_describer.update_picture()
    image_paths = [
            # "images/pantry.jpg", "images/recycling.jpg",
            # "images/laundry.png", "images/gardening.jpg",
            # "images/bike.jpg", "images/breakfast.jpg"
            "images/test_photo.jpg"
            ]
    
    for question, image_path in zip(questions, image_paths):
        logger.info(f"Generating description for question: {question}")
        description = image_describer.generate_description(question, image_path).split("Description: ")[-1]
        logger.info(f"Generated description: {description}")
    
        print(description)