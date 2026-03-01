from ray import serve
from transformers import pipeline
from starlette.requests import Request

@serve.deployment
class BatchedTranslationModel:

    def __init__(self):
        self._model = pipeline(
            "translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr"
        )

    @serve.batch(max_batch_size=8, batch_wait_timeout_s=0.1)
    async def handle_batch(self, strings: list[str]) -> list[str]:
        print(f"batch size: {len(strings)}")
        return self._model(strings)

    async def __call__(self, request: Request) -> list[str]:
        return await self.handle_batch(request.query_params["text"])


app = BatchedTranslationModel.bind()
