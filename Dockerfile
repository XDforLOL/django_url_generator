# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc python3-dev musl-dev \
    && apt-get clean

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
