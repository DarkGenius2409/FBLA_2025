from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, model_validator
from langchain_core.output_parsers import JsonOutputParser
import time

# Global Variables
model = OllamaLLM(model="llama3.1")
actionTypes = ["speak", "leave", "move"]
characters = ["fbi-agent", "prisoner"]

class Action(BaseModel):
    character: str = Field(description="Name of character doing the action")
    actionType: str = Field(description="Type of action")
    target: str = Field(description="Dialogue spoken, target character, or empty depending on action type")

    @model_validator(mode="after")
    def validate_action(self):
        if self.actionType not in actionTypes:
            raise ValueError(f"'actionType' must be one of {actionTypes}. Got: {self.actionType}")

        if self.actionType == "speak" and not self.target:
            raise ValueError("'target' must contain dialogue for 'speak' action")
        if self.actionType == "move" and  self.target == "":
            raise ValueError("'target' must specify the target character for 'move' action")
        if self.actionType == "move" and self.target not in characters:
            raise ValueError("'target' must be a valid character for 'move' action")
        if self.actionType == "leave" and self.target:
            raise ValueError("'target' must be empty for 'leave' action")

        return self



class Scene(BaseModel):
    actions: list[Action] = Field(description="List of actions for the story in order")
    characters: list[str] = Field(description="List of characters in the scene")
    backdrop: str = Field(description="The backdrop")

    @model_validator(mode='after')
    def validate_scene(self):
        # Validate all characters in the scene list
        for character in self.characters:
            if character not in characters:
                raise ValueError(
                    f"Invalid character '{character}' in scene characters list. Valid characters are: {characters}")

        # Also validate characters used in actions
        for action in self.actions:
            if action.character not in characters:
                raise ValueError(
                    f"Invalid character '{action.character}' in action. Valid characters are: {characters}")

            # For move actions, validate the target character
            if action.actionType == "move" and action.target not in characters:
                raise ValueError(
                    f"Invalid target character '{action.target}' in move action. Valid characters are: {characters}")

            # Ensure the character performing the action is listed in the scene's characters
            if action.character not in self.characters:
                raise ValueError(
                    f"Character '{action.character}' performs an action but is not listed in scene characters")

        return self


class Story(BaseModel):
    scenes: list[Scene] = Field(description="List of scenes in the story")
    question: list[str] = Field(
        description="A list of four choices the user can select from",
    )
    summary: str = Field(
        description="A short summary of everything that happened so far.",
    )
    end: bool = Field(
        description="Whether the story should end or not.",
    )

    @model_validator(mode='after')
    def validate_story(self):
        for scene in self.scenes:
            if not set(scene.characters).issubset(set(characters)):
                raise ValueError(f"Scene contains invalid characters")
        if len(self.question) <= 2:
            raise ValueError("There must be >2 choices provided.")

        return self

class Topics(BaseModel):
    topics: list[str] = Field(description="List of topics")

def getDataInFormat(chain, model, input_data, max_attempts=5, delay=2):
    attempt = 0
    while attempt < max_attempts:
        try:
            response = chain.invoke(input_data)
            model.model_validate(response)

            return response
        except Exception as e:
            print(e)

            attempt += 1
            if attempt < max_attempts:
                time.sleep(delay)
            else:
                print("Max attempts reached. Unable to get a successful response.")
                raise


def createTopics():
    parser = JsonOutputParser(model=Topics)

    prompt_template = """
        You are a helpful assistant. Your task is to create a list of 3-5 ORIGINAL story topics. 
        They should be simple and be a a short sentence long (<10 words)
        Your stories should feature minimum of 2 of the following characters: {characters}
        
        Create NEW, UNIQUE topics - do not copy the examples below.
        DO NOT create stories that involve any other characters  than: {characters}
        
        Follow this exact format:
        {{
            "topics": ["topic 1", "topic 2", "topic 3", "topic 4"]
        }}

        Reply only with the valid JSON.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model | parser

    return getDataInFormat(chain, Topics,{"characters": characters})

def createStory(topic, endStory=False):
    parser = JsonOutputParser(model=Story)

    action = f"Your task is to create a JSON object continuing a story. So far, {topic}. Continue the story"

    if endStory:
        action = f"Your task is to create a JSON object ending this story. {topic}. Think of a fitting scene to end the story at "

    # Define the prompt with proper escaping
    prompt_template = """
    You are a helpful assistant. {action}
    Use the following characters: {characters} as actors in the story.
    
    For the question in the story JSON object, it should be used to determine what happens next in the story. THIS IS VERY IMPORTANT
    The JSON must strictly adhere to the following format:
    {{
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
        "end":{end}
    }}

    Ensure the following:
    - All provided characters are included at least once in the story.
    - The actions are sequential and form a coherent narrative.
    - Each scene includes at least one action.
    - For the question in the story, it should be used to determine what happens next in the story. THIS IS VERY IMPORTANT
    - Follow the JSON format exactly as specified. Respond only with valid JSON. Do not include an introduction or summary.
    - Fit as many actions into one scene as possible while keeping all actions logical
    - Create a new scene only when a sufficient amount of time has passed since the previous scene or when different characters are performing actions simultaneously. Combine actions into a single scene if they can logically occur within the same timeframe.
    """


    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_template)
    ])
    print(action)

    chain = prompt | model | parser
    return getDataInFormat(chain, Story, {"characters": characters,  "action": action, "end":endStory})

