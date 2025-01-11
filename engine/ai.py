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

    @model_validator(mode="after")
    def validate_action(self):
        for character in self.characters:
            if character not in characters:
                raise ValueError("Invalid Character")
        return self

class Story(BaseModel):
    scenes: list[Scene] = Field(description="List of scenes in the story")

def getDataInFormat(chain, input_data, max_attempts=5, delay=2):
    attempt = 0
    while attempt < max_attempts:
        try:
            print(f"Attempt {attempt}")
            response = chain.invoke(input_data)
            return response
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(delay)
            else:
                print("Max attempts reached. Unable to get a successful response.")
                raise

def createStory(topic):
    parser = JsonOutputParser(model=Story)

    # Define the prompt with proper escaping
    prompt_template = """
    Write a short story.
    You are a helpful assistant. Your task is to create a JSON object describing a short story about {topic} 
    Use the following characters: {characters} as actors in the story.

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
        ]
    }}

    Ensure the following:
    - All provided characters are included at least once in the story.
    - The actions are sequential and form a coherent narrative.
    - Each scene includes at least one action.
    - Follow the JSON format exactly as specified. Respond only with valid JSON. Do not include an introduction or summary.
    - Fit as many actions into one scene as possible while keeping all actions logical
    - Create a new scene only when a sufficient amount of time has passed since the previous scene or when different characters are performing actions simultaneously. Combine actions into a single scene if they can logically occur within the same timeframe.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_template)
    ])

    chain = prompt | model | parser
    return getDataInFormat(chain, {"characters": characters, "topic": topic})

