# Use an official Python 3.14 runtime as the base image
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder
COPY . .

# Expose port 5000 (Flask's default port)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]