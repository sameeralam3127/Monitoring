import logging
import os
import random
import time

from flask import Flask, jsonify
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "python-observability-demo")
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
OTEL_SDK_DISABLED = os.getenv("OTEL_SDK_DISABLED", "").lower() == "true"

resource = Resource.create(
    {
        "service.name": SERVICE_NAME,
        "service.version": "1.0.0",
        "deployment.environment": os.getenv("DEPLOYMENT_ENVIRONMENT", "local"),
    }
)

trace_provider = TracerProvider(resource=resource)
if not OTEL_SDK_DISABLED:
    trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT)))
    trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)

metric_readers = []
if not OTEL_SDK_DISABLED:
    metric_readers.append(
        PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=OTLP_ENDPOINT),
            export_interval_millis=5000,
        )
    )
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=metric_readers))
meter = metrics.get_meter(__name__)

logger_provider = LoggerProvider(resource=resource)
if not OTEL_SDK_DISABLED:
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=OTLP_ENDPOINT)))
set_logger_provider(logger_provider)

request_counter = meter.create_counter(
    "demo_requests_total",
    description="Total requests handled by the Python OpenTelemetry demo app.",
)
latency_histogram = meter.create_histogram(
    "demo_request_latency_seconds",
    unit="s",
    description="Request latency for the Python OpenTelemetry demo app.",
)

LoggingInstrumentor().instrument(set_logging_format=True)
logging.basicConfig(level=logging.INFO)
if not OTEL_SDK_DISABLED:
    logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))
logger = logging.getLogger(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


@app.get("/")
def index():
    start = time.perf_counter()
    status = "ok"

    with tracer.start_as_current_span("demo.work") as span:
        simulated_work = random.uniform(0.02, 0.2)
        time.sleep(simulated_work)
        span.set_attribute("demo.work.duration_seconds", simulated_work)
        logger.info("Handled demo request in %.3f seconds", simulated_work)

    latency = time.perf_counter() - start
    request_counter.add(1, {"route": "/", "status": status})
    latency_histogram.record(latency, {"route": "/", "status": status})

    return jsonify(
        {
            "service": SERVICE_NAME,
            "status": status,
            "latency_seconds": round(latency, 4),
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
