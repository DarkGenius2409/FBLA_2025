from engine.ai.schema import actionTypes, Topics, Story, backdrops
from engine.sprite import characters
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyDkzJl2M3CorRI35eKDcZkIJ3X-1PkGTJc")
model = genai.GenerativeModel("gemini-1.5-flash")


def askQuestion(question):
    prompt = f"""
     You are a helpful assistant for an organization called GemPlay. Here are the Frequently Asked Questions (FAQs):

     1. Why am I getting an error when I click a choice?
        Answer: Close the application and open it up again. These errors are rare and often closing and reopening the application works.

     2. How do I export the story?
        Answer: Once you are finished with the story or you click the 'exit' button, you will be prompted with an 'Export' button that will allow you to save a video of the story you made!

     3. Are the stories random?
        Answer: The stories are somewhat random, but not quite! This application utilizes an AI model that will be generating a story according to the choices you select. The choices you select will influence the movements of the character, the story plot, and the backdrops.

     4. I want to know more about how this application was coded. How do I contact?
        Answer: Email gemplay@gmail.com for any questions, comments, or concerns!

     The user asks: "{question}"

     Based on the above information, please respond to the user's question.
     Use the least amount of words possible. If nothing works, then just say 'I don't know'
     Just use alphanumeric characters!
     """

    response = model.generate_content(prompt)

    return response.text


def createTopics():
    prompt = f"""
        You are a helpful assistant. Your task is to generate a list of 3-5 ORIGINAL story topics that strictly adhere to the given constraints.
        
        - Each topic must involve **at least two** of the provided characters: {characters}.  
        - Each topic must take place within the given backdrops: {backdrops}.  
        - **Only use the listed characters**—do not introduce or reference any other entities (e.g., if "dragon" is not in {characters}, it cannot be mentioned).  
        - The story topics must be **logically feasible** within the provided backdrops.  
        - The topics must be **achievable using only the following actions**: {actionTypes}.  
        - Each topic must be a short sentence (<10 words).  
        - Generate **NEW, UNIQUE** topics that do not copy the examples below.  
        - Do not directly include the topics in the topic list
        - Each topic should be a simple coherent sentence, **do not use semicolons**
        
        Follow this exact format:
        Topics = {{
            "topics": ["topic 1", "topic 2", "topic 3", "topic 4"]
        }}

        Return Topics
    """

    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json"))
    data = json.loads(response.text)
    print(data)
    Topics.model_validate(data)
    return data


def createStory(topic, endStory=False):
    action = f"Your task is to create a JSON object continuing a story. So far, {topic}. Continue the story"

    if endStory:
        action = f"Your task is to create a JSON object ending this story. {topic}. Think of a fitting scene to end the story at "

    prompt = f"""
    You are a helpful assistant. {action}
    Use the following characters: {characters} as actors in the story.

    For the question in the story JSON object, it should be used to determine what happens next in the story. THIS IS VERY IMPORTANT
    The JSON must strictly adhere to the following format:
    Story = {{
        "scenes": [
            {{
                "characters": ["A list of characters involved in this scene. Must be a subset of {characters}. All characters directly or indirectly involved in the actions must be included in the scene"],
                "backdrop": "The backdrop of the scene. You can choose from {backdrops}",
                "actions": [
                    {{
                        "character": "The exact name of one of the characters in the scene",
                        "actionType": "One of these: speak, leave, move. The speak action means the character will say something, move means they will move to another character, and leave means they will leave the scene",
                        "target": "For 'speak', include the dialogue spoken by the character. For 'move', include the name of another character the actor is moving towards (must be one of {characters}). For 'leave', leave this field empty. THIS MUST BE A STRING."
                    }}
                ]
            }}
        ],
        "question":["next possibility 1", "next possibility 2", "next possibility 3", "next possibility 4"],
        "summary":"a detailed summary of everything that has happened. ensure to include every action that occurred in a concise manner, because this will be looked at to determine what happens next",
        "end":{endStory}
    }}

    Ensure the following:
    - All provided characters are included at least once in the story.
    - The actions are sequential and form a coherent narrative.
    - Each scene includes at least one action.
    - For the question in the story, it should be used to determine what happens next in the story. THIS IS VERY IMPORTANT
    - Follow the JSON format exactly as specified. Respond only with valid JSON. Do not include an introduction or summary.
    - Fit as many actions into one scene as possible while keeping all actions logical
    - Create a new scene only when a sufficient amount of time has passed since the previous scene or when different characters are performing actions simultaneously. Combine actions into a single scene if they can logically occur within the same timeframe.

    Return: Story
    """

    response = model.generate_content(prompt,
                                      generation_config=genai.GenerationConfig(response_mime_type="application/json"))
    data = json.loads(response.text)
    print(data)
    try:
        Story.model_validate(data)
        return data
    except:
        raise ValueError()



