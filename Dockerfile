# Use an official Python image as the base
FROM python:3.10-slim

# Set environment variables
ARG DATABASE_NAME \
    DATABASE_USER \
    DATABASE_PASSWORD \
    DATABASE_HOST \
    DATABASE_PORT \
    SECRET_KEY

ENV SECRET_KEY=${SECRET_KEY} \
    DATABASE_NAME=${DATABASE_NAME} \
    DATABASE_USER=${DATABASE_USER} \
    DATABASE_PASSWORD=${DATABASE_PASSWORD} \
    DATABASE_HOST=${DATABASE_HOST} \
    DATABASE_PORT=${DATABASE_PORT} 

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip and upgrade it
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput


# Expose the Django default port
EXPOSE 8000

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
