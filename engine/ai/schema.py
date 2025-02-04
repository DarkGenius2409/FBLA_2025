from pydantic import BaseModel, Field, model_validator
from engine.sprite import characters

actionTypes = ["speak", "leave", "move"]
backdrops = ["castle", "cave", "desert", "lake", "village", "village2"]
music = ["chill1", "chill2", "battle1", "battle2"]

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
        if self.actionType == "move" and self.target not in characters.keys():
            raise ValueError("'target' must be a valid character for 'move' action")
        if self.actionType == "leave" and self.target:
            raise ValueError("'target' must be empty for 'leave' action")

        return self



class Scene(BaseModel):
    backdrop: str = Field(description="The backdrop")
    music: str = Field(description="The music choice")
    actions: list[Action] = Field(description="List of actions for the story in order")
    characters: list[str] = Field(description="List of characters in the scene")

    @model_validator(mode='after')
    def validate_scene(self):
        # Validate all characters in the scene list
        for character in self.characters:
            if character not in characters:
                raise ValueError(
                    f"Invalid character '{character}' in scene characters list. Valid characters are: {characters}")

        if self.backdrop not in backdrops:
            self.backdrop = "castle"
            raise ValueError(
                f"Invalid backdrop")

        if self.music not in music:
            raise ValueError(
                f"Invalid music")

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