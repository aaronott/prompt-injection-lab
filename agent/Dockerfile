FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl python3 ca-certificates netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY agent.py .

ENV TARGET_URL=http://malicious-server:8000
ENV EXECUTE_PAYLOAD="false"

# Force unbuffered stdout/stderr and line-flush prints
ENV PYTHONUNBUFFERED=1

# Run Python unbuffered
CMD ["python3", "-u", "agent.py"]