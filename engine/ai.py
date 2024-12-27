
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, model_validator
from langchain_core.output_parsers import JsonOutputParser
import time

model = OllamaLLM(model="llama3.1")
actionTypes = ["speak", "leave", "move"]
characters = ["Donald Trump", "Joe Biden"]

class Action(BaseModel):
    character: str = Field(description="Name of character doing the action")
    actionType: str = Field(description="Type of action")
    target: str = Field(description="Dialogue spoken by the actor")

    @model_validator(mode="after")
    def validate_action(self):
        if self.actionType not in actionTypes:
            raise ValueError(f"'actionType' must be one of {actionTypes}. Got: {self.actionType}")

        if self.actionType == "speak" and not self.target:
            raise ValueError("'target' must contain dialogue for 'speak' action")
        if self.actionType == "move" and not self.target:
            raise ValueError("'target' must specify the target character for 'move' action")
        if self.actionType == "move" and not (self.target in characters):
            raise ValueError("'target' must be a target character for 'move' action")
        if self.actionType == "leave" and self.target:
            raise ValueError("'target' must be empty for 'leave' action")

        return self  # Must return the validated instance

class Scene(BaseModel):
    actions: list[Action] = Field(description="List of actions for the story in order")

# Retry Logic Function
def getDataInFormat(chain, input_data, max_attempts=5, delay=2):
    attempt = 0
    while attempt < max_attempts:
        try:
            print(f"Attempt {attempt}")
            response = chain.invoke({
                **input_data
            })
            return response  # Return the response if successful
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_attempts:
                time.sleep(delay)  # Wait before retrying
            else:
                print("Max attempts reached. Unable to get a successful response.")
                raise

def createStory(topic):
    parser = JsonOutputParser(model=Scene)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """
         Write a short story.
         You are a helpful assistant. Your task is to create a JSON object describing a short story abouut {topic} 
         Use the following characters: {characters} as actors in the story.

         The JSON must strictly adhere to the following format:
         {{
             "actions": [
                 {{
                     "character": "The exact name of one of the characters provided",
                     "actionType": "One of these: speak, leave, move. The speak action means the character will say something, move means they will move to another character, and leave means they will leave the scene",
                     "target": "For 'speak', include the dialogue spoken by the character. For 'move', include the name of another character the actor is moving towards (must be one of {characters}). For 'leave', leave this field empty. THIS MUST BE A STRING.",
                 }},
                 ...
             ]
         }}

         Ensure the following:
         - All provided characters are included at least once in the story.
         - The actions are sequential and form a coherent narrative.
         - Follow the JSON format exactly as specified. Respond only with valid JSON. Do not include an introduction or summary.
         """)
    ])


    chain = prompt | model | parser
    return getDataInFormat(chain, {"characters":characters, "topic":topic})


