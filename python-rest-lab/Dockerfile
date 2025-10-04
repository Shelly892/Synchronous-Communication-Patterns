# Use Python official image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Flask default 5000)
EXPOSE 5000

# Set environment variables
ENV RUN_MODE=app

# Default command to run Flask application
# CMD ["python", "app.py"]
CMD ["sh", "-c", "python ${RUN_MODE}.py"]