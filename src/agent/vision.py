from .agent import Agent


class Vision(Agent):
    """
        a vision agent should able to visually watch something
        in the base case it can watch video or photos provides by the user 
    """
    def __init__(self, model):
        self.model = model

    def run(self, task):
        pass
