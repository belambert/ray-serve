# Ray Serve Batched Sentiment Analysis

A Ray Serve application that deploys a batched sentiment analysis model using Hugging Face Transformers.

## Installation

```bash
poetry install
```

## Usage

### Start the server

```bash
poetry run serve run ray_serve.main:app
```

### Make requests

Single request:

```bash
curl "http://localhost:8000?text=happy"
```

Multiple concurrent requests to trigger batching:

```bash
for i in `seq 1 10`; do; curl "http://localhost:8000?text=happy" &; done;
```

## Architecture

- **Model**: Hugging Face sentiment-analysis pipeline
- **Batching**: Ray's `@serve.batch` with max batch size 8 and 0.1s timeout
- **Input**: Text via query parameter `text`
- **Output**: List of sentiment analysis results

## Related Documentation

- [Ray Serve Overview](https://docs.ray.io/en/latest/serve/index.html)
- [Ray Serve Getting Started](https://docs.ray.io/en/latest/serve/getting_started.html)
- [Ray Serve Performance Guides](https://docs.ray.io/en/latest/serve/advanced-guides/performance.html)
- [Dynamic Request Batching](https://docs.ray.io/en/latest/serve/advanced-guides/dyn-req-batch.html)
