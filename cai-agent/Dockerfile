FROM python:3.12-slim

# tools CAI agents commonly call
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl netcat-traditional ca-certificates git \
  && rm -rf /var/lib/apt/lists/*

# install CAI
RUN pip install --no-cache-dir cai-framework

# helpful: unbuffered output
ENV PYTHONUNBUFFERED=1 \
    CAI_STREAM=false

WORKDIR /workspace
CMD ["bash", "-lc", "cai"]
