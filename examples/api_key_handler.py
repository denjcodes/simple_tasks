from groq import Groq
import os

def generate_client(API_KEY):
    # Initialize the Groq client
    # client = Groq(api_key=os.environ['GROQ'])
    client = Groq(api_key=API_KEY)
    return client