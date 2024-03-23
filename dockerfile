# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir Flask requests

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
