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
ENV FLASK_APP=app.py

# Default command to run Flask application
CMD ["python", "app.py"]