# Stage 1: Build stage
FROM python:3.8-slim AS builder

# Set working directory
WORKDIR /app

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install build dependencies and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Runtime stage
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "catalogapp.wsgi:application"]
