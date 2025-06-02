from abc import ABC, abstractmethod


class Model(ABC):
    """
    This is an abstraction class for models
    Model can be any LLM or VLM
    """

    @abstractmethod
    def __init__(self):
        pass

    """
        Completion is 
        Args:
            query: query can be a prompt or RAG sentence
        Output:
            return a string response
    """

    @abstractmethod
    def completion(self, query: str) -> str:
        pass

    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def get_model(self):
        pass