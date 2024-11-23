import torch
from transformers import MllamaForConditionalGeneration, AutoProcessor
import base64

model_id = "meta-llama/Llama-3.2-90B-Vision"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(model_id)

def prompt(question):
    return f"""<|image|><|begin_of_text|>You are a Image Analyzer, specifically designed to create clear and focused descriptions for images based on user questions. Your role is to:

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

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# prompt = "<|image|><|begin_of_text|>If I had to write a haiku for this one"
# inputs = processor(image, prompt, return_tensors="pt").to(model.device)

# output = model.generate(**inputs, max_new_tokens=100)
# print(processor.decode(output[0]))


if __name__ == "__main__":    
    questions = [
            "What types of food items and containers are present in the pantry, and how are they currently arranged on the shelves?",
            "What objects in the scene are made of paper, plastic, glass, or metal, and how are they currently disposed of (e.g., in trash or recycling bins)?",
            "What types of clothing, including their dominant colors and fabric care labels, are visible in the laundry pile?",
            "What plants and weeds are in the gardening area, and what is their condition - e.g., are they healthy, dry, or overgrown?",
            "What components of the bicycle (such as wheels, brakes, gears, or chain) appear damaged or worn out, and what tools or spare parts might be needed to repair them in the surrounding workspace or storage area?",
            "What edible items, such as fruits, bread, eggs, or breakfast cereals, are visible on the countertops or in the open cabinets in the kitchen?",
            ]
    


    image_paths = [
            "images/pantry.jpg", "images/recycling.jpg",
            "images/laundry.png", "images/gardening.jpg",
            "images/bike.jpg", "images/breakfast.jpg"
            ]
    
    for question, image_path in zip(questions, image_paths):
        inputs = processor(encode_image(image_path), prompt(question), return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=100)
        description = processor.decode(output[0])

        # description = image_describer.generate_description(question, image_path).split("Description: ")[-1]
        # logger.info(f"Generated description: {description}")
    
        print(description)