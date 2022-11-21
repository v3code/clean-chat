import uuid
from abc import ABC, abstractmethod


class ToxicityPredictorConnector(ABC):

    @abstractmethod
    def send_to_check(self, message_id: uuid.UUID, content: str):
        pass