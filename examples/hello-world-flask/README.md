# hello-world-flask

This simple Flask app that returns "Hello World". This app configures OpenTelemetry to send data to Honeycomb using the `opentelemetry_instrument` command and environment variables.

It also contains examples of:

- sending metrics with OpenTelemetry using a counter
- using baggage with context tokens
- manually passing baggage with context
- setting a span attribute

If you are looking for an example using the `configure_opentelemetry()` function and parameters, check out [hello-world app](../hello-world/README.md).

## Prerequisites

You'll also need [Poetry](https://python-poetry.org/) installed to run the example. Poetry automatically creates a virtual environment to run the example in so you don't need to manage one yourself.

## Running the example

Install the dependencies:

```bash
poetry install
```

Run the application:

```bash
SERVICE_NAME=hello_world_flask poetry run flask run --port 5219
```

Now you can `curl` the app:

```bash
$ curl localhost:5219
Hello World
```

## Distro Instrumentation Example

To send traces to local console:

```bash
OTEL_SERVICE_NAME=hello_world_flask DEBUG=true poetry run opentelemetry-instrument flask run --port 5219
```

