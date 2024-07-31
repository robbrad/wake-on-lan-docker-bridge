# Use the official Python image from the Docker Hub
FROM python:alpine

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY wol_listener.py .

# Expose the correct port
EXPOSE 55555

# Run the Python script when the container starts
CMD ["python", "wol_listener.py"]