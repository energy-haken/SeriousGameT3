from abc import abstractmethod, ABC


class DialogObjectObserver(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update_doo(self,subject,data_type,data) -> None:
        """
        Receive update from subject.
        """
        pass






