# Use the official Python image from the Docker Hub
FROM python:3.11

# Install the necessary packages
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install uwsgi
RUN pip install uwsgi

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]