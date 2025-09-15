from abc import abstractmethod, ABC


class ModelObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self,subject,data_type,data) -> None:
        """
        Receive update from subject.
        """
        pass






