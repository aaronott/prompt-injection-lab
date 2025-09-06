FROM python:3.12-slim
WORKDIR /app

# add netcat so the decoded reverse shell can run
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir openai==1.43.0 "httpx<0.28" requests==2.32.3
COPY agent.py .
ENV PYTHONUNBUFFERED=1
