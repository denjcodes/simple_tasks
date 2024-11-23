Task Breakdown for ADHD & Down Syndrome Patients

High Level Idea

- Take an image and ask for the high level task
- Ask Llama to identify key components to complete the task and all visual information needed to complete the task
- Generate prompts to detect items inside the picture or take another picture.
- Given the task, break down the normal task and then curate the output to be based upon items identified
- Interview to ask questions about the task to avoid making assumptions.

Tasks:

- How to prompt Llama with an image (done) (image_describer.py)
- Prompt Engineering
    - Persona
    - Few-shots (Optional)
    - Chain of Thought
    - RAG
    - Interview
- Generate question prompts using Llama (image_question_generator.py)
- Ask user about what they see (image_requestor.py)
- Text to speech (done)
- Speech to Text (done)
- Integration with Camera
- 

Agent to generate prompts for image questioning

Agent to question the image for details

Agent to break down the text





User: I want to clean the table

Questioner          (I want to clean the table): What do you see on the table?
Picture Requestor   (I want to clean the table): Can you take a picture of the table?

Describer           (Picture of Table)+(What do you see on the table): I see a plate, a fork, a knife, a glass, and a napkin on the table.


Example for memory task:
<Persona for task breaker>
Task: <task>
Query: <query>
Description: <description>
Steps:
- <step 1>
- <step 2>
- <step 3>
...

"""Memory element"""
User: Given a list of steps, choose the first one to perform
Assistant: Step 1: <step 1>
User: Step 1 complete.
User: Scene Description: <scene description>. Based on the current scene, are we on the right track? What is the next step?
Assistant: Great! We are/arenot on the right track. The next step is <step 2>.
User: Step 2 complete.
User: Scene Description: <scene description>. Based on the current scene, are we on the right track? What is the next step?
Assistant: Great! We are/arenot on the right track. The next step is <step 3>.
...
