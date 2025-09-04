FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Listen forever on port 4444; -k keeps it open for multiple connections
CMD ["nc.traditional", "-lvkp", "4444"]
