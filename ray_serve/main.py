from typing import Dict

from ray import serve
from starlette.requests import Request
from transformers import pipeline


@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]


app = SentimentAnalysisDeployment.bind()
