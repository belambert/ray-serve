import time

from ray import serve
from ray.serve.handle import DeploymentHandle
from transformers import pipeline


@serve.deployment
class BatchedSentimentModel:

    def __init__(self):
        self._model = pipeline("sentiment-analysis")

    @serve.batch(max_batch_size=8, batch_wait_timeout_s=0.1)
    async def __call__(self, strings: list[str]) -> list[str]:
        return self._model(strings)


handle: DeploymentHandle = serve.run(BatchedSentimentModel.bind())
responses = [handle.remote(i) for i in ["happy"] * 16]
print(list(r.result() for r in responses))

time.sleep(99999)
