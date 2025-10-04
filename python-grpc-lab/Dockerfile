# Use Python official image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

ENV RUN_MODE=server
# Expose port 
EXPOSE 50051


# Default command to run Flask application
# CMD ["python", "server.py"]
CMD ["sh", "-c", "python ${RUN_MODE}.py"]






