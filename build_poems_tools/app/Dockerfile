# Use an official Python runtime as the base image
FROM python:3.11-slim

ENV PORT=5000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the entrypoint command to run the Flask app using Gunicorn server
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD gunicorn --bind :$PORT app:app

