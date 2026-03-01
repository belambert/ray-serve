# Ray Serve example

A Ray Serve example application. Deploys two models with
dynamic request batching using Hugging Face Transformers:

- **Sentiment analysis** — classifies text as positive or
  negative.
- **Translation (EN → FR)** — translates English text to
  French using Helsinki-NLP/opus-mt-en-fr.

Concurrent requests are automatically grouped into batches
for improved throughput.

## How it works

Each deployment wraps a Hugging Face pipeline in a Ray
Serve deployment. Ray's `@serve.batch` decorator accumulates
incoming requests and processes them together, reducing
per-request overhead.

**Batching parameters (both deployments):**

- **Max batch size**: 8 — up to 8 requests are grouped into
  a single inference call.
- **Batch wait timeout**: 0.1s — if fewer than 8 requests
  arrive, the batch fires after 100ms.

**Request flow:**

1. Client sends a GET request with a `text` query parameter.
2. Ray Serve routes the request to the appropriate
   deployment based on the route prefix.
3. The `handle_batch` method collects requests until the
   batch is full or the timeout expires.
4. The Hugging Face pipeline runs inference on the entire
   batch at once.
5. Each client receives its individual result.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
uv sync
```

## Usage

### Start the server

```bash
uv run serve run config.yaml
```

On first run, the Hugging Face models are downloaded and
cached automatically.

### Make requests

Sentiment analysis:

```bash
curl "http://localhost:8000/sentiment?text=happy"
```

Example response:

```json
[{"label": "POSITIVE", "score": 0.9998}]
```

Translation (EN → FR):

```bash
curl "http://localhost:8000/translation?text=hello world"
```

Example response:

```json
[{"translation_text": "Bonjour le monde"}]
```

Multiple concurrent requests to trigger batching:

```bash
for i in `seq 1 10`; do
  curl "http://localhost:8000/sentiment?text=happy" &
done
```

When batching activates, the server logs `batch size: N`
showing how many requests were grouped.

## Project Structure

```
ray_serve/
├── __init__.py
├── sentiment.py     # sentiment analysis deployment
└── translation.py   # EN→FR translation deployment
tests/
├── __init__.py
config.yaml          # Ray Serve multi-app config
pyproject.toml       # dependencies and project config
start.sh             # server startup shortcut
curl.sh              # example request shortcuts
```

## Dependencies

| Package        | Purpose                                |
| -------------- | -------------------------------------- |
| `ray[serve]`   | Model serving with request batching    |
| `transformers` | Pre-trained ML pipelines               |
| `torch`        | PyTorch backend for transformers       |
| `numpy`        | Numerical computing (torch dependency) |

## Related Documentation

- [Ray Serve Overview](https://docs.ray.io/en/latest/serve/index.html)
- [Ray Serve Getting Started](https://docs.ray.io/en/latest/serve/getting_started.html)
- [Dynamic Request Batching](https://docs.ray.io/en/latest/serve/advanced-guides/dyn-req-batch.html)
- [Ray Serve Performance Guides](https://docs.ray.io/en/latest/serve/advanced-guides/performance.html)
