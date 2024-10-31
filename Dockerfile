# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production  \
    LANGCHAIN_TRACING_V2=true \
    LANGCHAIN_PROJECT=intent-2-transaction \
    API_URL=https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo


# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Create a non-root user and switch to it for security
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 5000


# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Command to run the application
# Command to run the application using Flask directly
CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0"]