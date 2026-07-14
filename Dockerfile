FROM python:3.12-slim

WORKDIR /app

# Install build deps for asteri C extension
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn

# Remove build deps
RUN apt-get purge -y --auto-remove gcc python3-dev && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . .

# Remove docker dir
RUN rm -rf docker/

EXPOSE 8888

ENV DOCKER=1

CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8888", "--workers", "2"]
