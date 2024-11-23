from groq import Groq
import base64
import os
import api_key_handler

# Initialize the Groq client
# client = Groq(api_key=os.environ['GROQ'])
client = api_key_handler.generate_client(api_key=os.environ['GROQ'])

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your local image
image_path = "/Users/dj/Documents/GitHub/groq-python/image0.jpg"

# Encode the image
base64_image = encode_image(image_path)

# Create the chat completion request
completion = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "I am intellectually disabled person and I need help with simple tasks.  Using this picture, help me to clean this table"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

# Print the assistant's response
print(completion.choices[0].message.content)

