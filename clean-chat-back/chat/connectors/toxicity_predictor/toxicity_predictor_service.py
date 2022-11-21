import uuid

from chat.connectors.toxicity_predictor.toxicity_predictor_core import ToxicityPredictorConnector
from core.singleton import Singleton


class ToxicityPredictorServiceConnector(ToxicityPredictorConnector, Singleton):

    

    def send_to_check(self, message_id: uuid.UUID, content: str):
        pass