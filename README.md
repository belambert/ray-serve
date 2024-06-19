

See:
- https://docs.ray.io/en/latest/serve/index.html
- https://docs.ray.io/en/latest/serve/getting_started.html
- https://docs.ray.io/en/latest/serve/advanced-guides/performance.html
- https://docs.ray.io/en/latest/serve/advanced-guides/dyn-req-batch.html



## batched version

To run:

    poetry run serve run ray_serve.main:app

To curl:

    curl "http://localhost:8000?text=happy"

To trigger batching curl like this:

    for i in `seq 1 10`; do; curl "http://localhost:8000?text=happy" &; done;


## misc

To show metrics in the dashboard: https://docs.ray.io/en/latest/cluster/metrics.html
