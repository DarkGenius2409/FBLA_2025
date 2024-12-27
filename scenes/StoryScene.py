from engine.scene import SceneBase


class StoryScene(SceneBase):
    def __init__(self, window, story):
        super().__init__(window)
        self.story = story


    def Update(self, events, keys):
        self.window.screen.fill((255,255,0))
