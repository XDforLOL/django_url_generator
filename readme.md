# URL Shortener Project

This project is a URL shortener service built with Django and PostgreSQL.
It allows users to create short URLs that redirect to long URLs. The project is containerized using Docker.

## Prerequisites

- Docker
- Docker Compose
- Django-secret key

## After clonnig the repository

you can create Secret key by running the following command in the terminal
in a python venv with a django environment installed
    ``` python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' ```
    It will generate a secret key that you can use in the settings.py file or you add it to the .env file

    ``` SECRET_KEY=your_secret_key ```

## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build and run the Docker containers:**
   After downloading and installing docker run this command to build the Django server and DB
    ```
    docker-compose up --build
    ```

## Usage

1. **Access the Django development server:**
    Open your browser and go to `http://localhost:8000`.

2. **Create a short URL:**
    Send a POST request to `/create` with the long URL in the request body:
    ```json
    {
        "url": "https://www.example.com"
    }
    ```

3. **Redirect to the long URL:**
    Access the short URL in your browser, e.g., `http://localhost:8000/s/<result from url creation>`.

## Running Tests
    The Tests run as soon as you build the docker compose file

## Project Structure

- `django_util`: Has two functions which provide utility to other functions
    A hashing function whcih shorthens the urls, and a URL validators
- `Dockerfile`: Defines the Docker image for the Django application.
- `docker-compose.yml`: Defines the Docker services for the project.
- `settings.py`: Django settings file, including database configuration .
- `url_manager/models.py`: Django models for the URL shortener.
- `url_manager/tests.py`: Unit tests for the URL shortener.

## License

This project is licensed under the MIT License.
