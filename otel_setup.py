from opentelemetry import trace, metrics, _logs
from opentelemetry.sdk.resources import Resource

# Traces
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Logs
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

from opentelemetry.instrumentation.logging import LoggingInstrumentor

import logging


def setup_otel():
    resource = Resource.create({"service.name": "otel-demo-app"})

    # -------- TRACES --------
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)

    trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")

    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    # -------- METRICS --------
    metric_exporter = OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")

    metric_reader = PeriodicExportingMetricReader(metric_exporter)

    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

    metrics.set_meter_provider(meter_provider)

    # -------- LOGS --------
    log_exporter = OTLPLogExporter(endpoint="http://localhost:4318/v1/logs")

    logger_provider = LoggerProvider(resource=resource)
    _logs.set_logger_provider(logger_provider)

    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    # Correlate logs with traces
    LoggingInstrumentor().instrument(set_logging_format=True)

    logging.basicConfig(level=logging.INFO)
