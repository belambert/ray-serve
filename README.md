

See:
- https://docs.ray.io/en/latest/serve/index.html
- https://docs.ray.io/en/latest/serve/getting_started.html
- https://docs.ray.io/en/latest/serve/advanced-guides/performance.html
- https://docs.ray.io/en/latest/serve/advanced-guides/dyn-req-batch.html



## non-batched version

To run:

    poetry run serve run ray_serve.main:app

To curl:

    curl "http://localhost:8000?text=happy"


## batched version

Just run:

    poetry run python ./ray_serve/batch.py


## misc

To show metrics in the dashboard: https://docs.ray.io/en/latest/cluster/metrics.html
