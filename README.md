# Test Task AI Clinic

This repository contains the test task for AI Clinic. Made by Elina Shramko.

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

- Git
- Docker
- Docker Compose
- Python (for pre-commit hooks)

### Installation

1. **Clone the repository:**

    ```bash
    git clone git@github.com:lin4lins/test_task_AI_Clinic.git
    cd test_task_AI_Clinic
    ```

2. **Set up environment variables:**

    - Create a `.env` file in the project root directory.
    - Use `.env.dist` as a template for your `.env` file.

3. **Install pre-commit hooks:**

    ```bash
    pip install pre-commit
    pre-commit install
    ```

### Docker Setup

1. **Build the Docker containers:**

    ```bash
    docker compose build
    ```

2. **Apply database migrations:**

    ```bash
    docker compose run api python manage.py makemigrations
    docker compose run api python manage.py migrate
    ```

3. **Start the Docker containers:**

    ```bash
    docker compose up
    ```

## Documentation

For detailed API documentation, visit: `/swagger/`


### Running Tests

To run the tests, use the following command:

```bash
docker compose run api python manage.py test
