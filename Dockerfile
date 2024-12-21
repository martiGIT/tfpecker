FROM python:3.12-slim

WORKDIR /app

COPY tfpecker.py .
COPY README.md .

ENTRYPOINT ["python", "tfpecker.py"]