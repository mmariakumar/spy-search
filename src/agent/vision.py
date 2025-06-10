from .agent import Agent

from ..utils import read_config

class Vision(Agent):
    """
        a vision agent should able to visually watch something
        in the base case it can watch video or photos provides by the user 
    """
    def __init__(self, model , db = "./local_files"):
        self.model = model
        
        config = read_config()
        self.db = config['db']

    async def run(self, task , data):
        """
            TODO: check the model capability first
            read task , read db / image 
            still using local files but check if it is a png / jpeg files first
            we need a place to save the image or diagram
        """
        pass

    async def get_recv_format(self):
        pass 

    async def get_send_format(self):
        pass 

    
