# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /api

# Copy the application code into the container
COPY /api /api

# Install Python dependencies
RUN pip install -r /api/requirements.txt

# Set environment variables
ENV DB_USER=testuser
ENV DB_PASSWORD=testpass
ENV DB_HOST=testhost
ENV DB_PORT=testport
ENV DB_NAME=testname

# Run the application
CMD ["python", "/api/app.py"]