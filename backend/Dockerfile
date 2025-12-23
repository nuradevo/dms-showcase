FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for build and pg_isready (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl netcat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: install spaCy model at build time (uncomment to enable)
# RUN python -m spacy download ru_core_news_sm || true

COPY . .

# copy run_start and make executable
COPY run_start.sh /app/run_start.sh
RUN chmod +x /app/run_start.sh

EXPOSE 8000

CMD ["/app/run_start.sh"]