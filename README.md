# Ray Serve Batched Sentiment Analysis

A Ray Serve application that deploys a sentiment analysis model with dynamic request batching using Hugging Face Transformers. Concurrent requests are automatically grouped into batches for improved throughput.

## How It Works

The app wraps a Hugging Face `sentiment-analysis` pipeline in a Ray Serve deployment. Ray's `@serve.batch` decorator accumulates incoming requests and processes them together, reducing per-request overhead.

**Batching parameters:**

- **Max batch size**: 8 — up to 8 requests are grouped into a single inference call.
- **Batch wait timeout**: 0.1s — if fewer than 8 requests arrive, the batch fires after 100ms.

**Request flow:**

1. Client sends a GET request with a `text` query parameter.
2. Ray Serve routes the request to `BatchedSentimentModel.__call__`.
3. The `handle_batch` method collects requests until the batch is full or the timeout expires.
4. The Hugging Face pipeline runs inference on the entire batch at once.
5. Each client receives its individual result.

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/)

## Installation

```bash
poetry install
```

## Usage

### Start the server

```bash
poetry run serve run ray_serve.main:app
```

On first run, the Hugging Face model (`distilbert-base-uncased-finetuned-sst-2-english`) is downloaded and cached automatically.

### Make requests

Single request:

```bash
curl "http://localhost:8000?text=happy"
```

Example response:

```json
[{"label": "POSITIVE", "score": 0.9998}]
```

Multiple concurrent requests to trigger batching:

```bash
for i in `seq 1 10`; do; curl "http://localhost:8000?text=happy" &; done;
```

When batching activates, the server logs `batch size: N` showing how many requests were grouped.

## Project Structure

```
ray_serve/
├── __init__.py
└── main.py          # Ray Serve deployment with batched inference
tests/
├── __init__.py
pyproject.toml       # dependencies and project config
start.sh             # server startup shortcut
curl.sh              # example request shortcut
```

## Dependencies

| Package        | Purpose                                 |
| -------------- | --------------------------------------- |
| `ray[serve]`   | Model serving with request batching     |
| `transformers` | Pre-trained sentiment analysis pipeline |
| `torch`        | PyTorch backend for transformers        |
| `numpy`        | Numerical computing (torch dependency)  |

## Related Documentation

- [Ray Serve Overview](https://docs.ray.io/en/latest/serve/index.html)
- [Ray Serve Getting Started](https://docs.ray.io/en/latest/serve/getting_started.html)
- [Dynamic Request Batching](https://docs.ray.io/en/latest/serve/advanced-guides/dyn-req-batch.html)
- [Ray Serve Performance Guides](https://docs.ray.io/en/latest/serve/advanced-guides/performance.html)
