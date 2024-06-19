import time

from ray import serve
from ray.serve.handle import DeploymentHandle
from transformers import pipeline
from starlette.requests import Request

@serve.deployment
class BatchedSentimentModel:

    def __init__(self):
        self._model = pipeline("sentiment-analysis")

    @serve.batch(max_batch_size=8, batch_wait_timeout_s=0.1)
    async def handle_batch(self, strings: list[str]) -> list[str]:
        print(f"batch size: {len(strings)}")
        return self._model(strings)

    async def __call__(self, request: Request) -> list[str]:
        return await self.handle_batch(request.query_params["text"])


app = BatchedSentimentModel.bind()


# NUM_QUERIES = 32
# handle: DeploymentHandle = serve.run(BatchedSentimentModel.bind())
# responses = [handle.remote(i) for i in ["happy"] * NUM_QUERIES]
# print(list(r.result() for r in responses))
# # sleep so the dashboard stays open for a while
# time.sleep(99999)
