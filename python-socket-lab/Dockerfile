# Use Python official image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

ENV APP=server 

# Expose port
EXPOSE 8080

# Default command to run socket server
# CMD ["python", "server.py"]
CMD ["sh", "-c", "python ${APP}.py"]