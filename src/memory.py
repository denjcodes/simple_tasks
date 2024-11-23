from groq import Groq
from collections import deque

class ConversationMemory:
    def __init__(self, limit=15):
        self.memory = deque(maxlen=limit)
    
    def add_interaction(self, interaction):
        """
        Adds a new interaction to memory.
        :param interaction: A dictionary representing a single interaction.
        """
        self.memory.append(interaction)
    
    def get_history(self):
        """
        Retrieves the conversation history as a list.
        """
        return list(self.memory)


class ImageQuestioningAgent:
    def __init__(self, memory_limit=15):
        self.memory = ConversationMemory(limit=memory_limit)
    
    def process_interaction(self, image_id, question, answer):
        """
        Processes a new interaction by saving it to memory.
        :param image_id: Identifier for the image.
        :param question: Generated question.
        :param answer: Answer from the user/system.
        """
        interaction = {
            "image_id": image_id,
            "question": question,
            "answer": answer
        }
        self.memory.add_interaction(interaction)
    
    def get_conversation_history(self):
        """
        Retrieves the stored conversation history.
        """
        return self.memory.get_history()



# Initialize the agent with a memory limit of 15
agent = ImageQuestioningAgent(memory_limit=15)

# Simulate some interactions
agent.process_interaction("image_001", "What is the main object in the image?", "A tree.")
agent.process_interaction("image_002", "What color is the sky?", "Blue.")

# Fetch conversation history
history = agent.get_conversation_history()
for interaction in history:
    print(interaction)


