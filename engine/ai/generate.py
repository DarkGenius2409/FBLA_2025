from selenium.webdriver.common.devtools.v85.css import Value

from engine.ai.schema import actionTypes, Topics, Story
from engine.sprite import characters
import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyDkzJl2M3CorRI35eKDcZkIJ3X-1PkGTJc")
model = genai.GenerativeModel("gemini-1.5-flash")


def createTopics():
    prompt = f"""
        You are a helpful assistant. Your task is to create a list of 3-5 ORIGINAL story topics. 
        They should be simple and be a a short sentence long (<10 words)
        Your stories should feature minimum of 2 of the following characters: {characters}
        
        Create NEW, UNIQUE topics - do not copy the examples below.
        DO NOT create stories that involve any other characters  than: {characters}
        Ensure the the story topic can be completed with just the the following actions: {actionTypes}
        
        Follow this exact format:
        Topics = {{
            "topics": ["topic 1", "topic 2", "topic 3", "topic 4"]
        }}

        Return Topics
    """

    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json"))
    data = json.loads(response.text)
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
                "backdrop": "The backdrop of the scene",
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
        "summary":"quick one sentence summary of everything that happened",
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

    try:
        Story.model_validate(data)
        return data
    except:
        raise ValueError()



