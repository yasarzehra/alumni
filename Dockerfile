FROM python:3.11-slim

WORKDIR /app

# Copy application source
COPY . /app

# Expose standard HTTP port
EXPOSE 80

# Run development server
CMD ["python", "server.py"]
