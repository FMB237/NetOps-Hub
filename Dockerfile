# Build stage
FROM python:3.12-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY . .

# Runtime stage
FROM python:3.12-slim

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Change ownership of application files to appuser
RUN chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]