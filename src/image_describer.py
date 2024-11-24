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
        return f"""You are a Vision model expert in analyzing image, specifically designed to answer user questions in a clear and focused response. Your role is to:

1. Accept a question from a user
2. Analyze the image to find relevant elements
3. Generate a precise description that answers the user's question

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

    def update_picture_end(self):
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
            "Where are you and what is in your pantry that you see? What types of items do you see (e.g. food containers, spices, canned goods)? What is the condition of these items (e.g. full, empty, expired)? Where exactly are they located (e.g. on shelves, in baskets) in the pantry?",
            "What is the scene you're looking at and what objects, such as paper, plastic, or glass, do you see that can be recycled? Can you describe something distinct about each object, and where are they located in the scene?",
            "What is the setting of your laundry area and what items of clothing do you see? Are they dirty or clean, and are any of them delicates? Where is each item located in relation to the washer, dryer, and any sorting bins?",
            "Describe the area you see for gardening. What objects, such as plants, tools, or gardening supplies, are present? What condition or unique characteristic can you describe about each of these objects? Where is each object located in the area?",
            "What is the environment around you like, and what items and tools related to your bike do you see? Is your bike in pieces or is it whole? Where exactly do you see your bike and the tools such as wrench, pliers, and the like?",
            "Where are you and what objects related to breakfast preparation do you see, such as appliances, food, or cooking tools? What unique characteristics (e.g. brand, size, color) can you describe for each object, and where are they located in your space?",
            # "What objects are on the table, and what is their condition in terms of dirtiness or clutter, to guide the cleaning process?"
            ]
    

    image_describer.update_picture()
    image_paths = [
            "images/test/pantry.jpg", "images/test/recycling.jpg",
            "images/test/laundry.png", "images/test/gardening.jpg",
            "images/test/bike.jpg", "images/test/breakfast.jpg"
            # "images/test_photo.jpg"
            ]
    
    for question, image_path in zip(questions, image_paths):
        logger.info(f"Generating description for question: {question}")
        description = image_describer.generate_description(question, image_path).split("Description: ")[-1]
        logger.info(f"Generated description: {description}")
    
        print(description)