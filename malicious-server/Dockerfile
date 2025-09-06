FROM python:3.11-alpine
WORKDIR /app
COPY server.py index.html ./
RUN apk add --no-cache curl
EXPOSE 8000
CMD ["python", "server.py"]
