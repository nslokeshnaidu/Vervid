from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for every AI agent in VeriVid.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, input_data):
        """
        Execute the agent's task.

        Parameters:
            input_data: The input required by the agent.

        Returns:
            The output produced by the agent.
        """
        pass