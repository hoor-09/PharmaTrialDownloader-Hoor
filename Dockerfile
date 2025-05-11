# Use official Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "validation.py"]
