from fastapi import FastAPI
import time
import logging

from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from otel_setup import setup_otel

# Init OTel
setup_otel()

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Tracer & Meter
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Metrics
request_counter = meter.create_counter(
    name="requests_total", description="Total number of requests"
)

latency_histogram = meter.create_histogram(
    name="request_latency", description="Request latency"
)

logger = logging.getLogger(__name__)


@app.get("/")
def root():
    start = time.time()

    with tracer.start_as_current_span("root-handler"):
        logger.info("Handling request")

        request_counter.add(1)

        duration = time.time() - start
        latency_histogram.record(duration)

        return {"message": "Hello, OpenTelemetry!"}
