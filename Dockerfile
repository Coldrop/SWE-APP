# Dockerfile
FROM python:3.11-slim

# System deps (optional: psycopg2, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# App directory
WORKDIR /app

# Copy & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy the rest
COPY . .

# Healthcheck (expects /health route; add it in Flask)
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1

# Expose gunicorn port
EXPOSE 8000

# Gunicorn entry (adjust module:app if needed)
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:8000", "app:app"]
