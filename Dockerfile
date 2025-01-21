# Use a lightweight Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . .

# Expose the port if the app is designed to run on a server
# (comment out if unnecessary)
# EXPOSE 8000

# Default command to run the application
CMD ["python", "main.py"]
