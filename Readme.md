# OpenTelemetry FastAPI Demo (with SigNoz)

A simple FastAPI application instrumented with OpenTelemetry to demonstrate traces, metrics, and logs, visualized using SigNoz.

## Prerequisites
1. Python 3.8+
2. Docker (for running SigNoz)

### 1. Setup Python Environment

`python -m venv venv`

`source venv/bin/activate` # Mac/Linux

Install dependencies:
```bash
pip install fastapi uvicorn opentelemetry-sdk opentelemetry-api \
opentelemetry-exporter-otlp \
opentelemetry-instrumentation-fastapi \
opentelemetry-instrumentation-logging
```

### 2. Setup SigNoz

Run SigNoz locally using Docker:

```bash
git clone https://github.com/SigNoz/signoz.git
cd signoz/deploy/docker

docker compose up -d
```

Access dashboard at: `http://localhost:8080`

### 3. Run the Application

Start FastAPI server: `uvicorn app:app --reload`

App will run on:

http://localhost:8000

### 4. Generate Telemetry

Send a request: `curl localhost:8000`

### 5. View Data in SigNoz

Go to: `http://localhost:8080`
