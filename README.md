# API Documentation AI Assistant

An AI-powered assistant for API documentation that helps users understand and interact with API specifications.

## Features

- Upload and parse OpenAPI/Swagger specifications
- Query specific endpoint details
- Ask natural language questions about the API
- AI-powered responses using OpenAI

## Project Structure

```
api-documentation-ai-assistant/
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── src/                  # Source code
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration settings
│   ├── main.py           # FastAPI application and routes
│   ├── models.py         # Pydantic data models
│   └── services.py       # Service implementations
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker configuration
├── LICENSE               # MIT License
├── pyproject.toml        # Poetry dependency management
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.13+
- Poetry (for dependency management)
- Docker and Docker Compose (optional, for containerized deployment)

### Setup

1. Clone the repository:

```bash
git clone git@github.com:anqorithm/api-documentation-ai-assistant.git
cd api-documentation-ai-assistant
```

2. Install dependencies:

```bash
poetry install
```

3. Create a `.env` file in the project root with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

### Using Poetry

Start the application:

```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at http://localhost:8080

### Using Docker

Build and run using Docker:

```bash
# Build the Docker image
docker build -t api-documentation-ai-assistant .

# Run the container
docker run -p 8080:8080 -e OPENAI_API_KEY=your_openai_api_key_here api-documentation-ai-assistant
```

### Using Docker Compose

Run with Docker Compose:

```bash
# Set your OpenAI API key in the environment or .env file
export OPENAI_API_KEY=your_openai_api_key_here

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Docker Compose Features

The enhanced Docker Compose configuration provides:

- **Health checks** - Automatic monitoring of service health
- **Resource management** - CPU and memory limits to prevent resource exhaustion
- **Persistent volumes** - Data persistence across container restarts
- **Network isolation** - Dedicated bridge network for security
- **Environment configuration** - Support for .env files and variable defaults
- **Robust restart policy** - Automatic service recovery

To check the service health:

```bash
docker-compose ps
```

To stop the service:

```bash
docker-compose down
```

To stop the service and remove volumes:

```bash
docker-compose down -v
```

## API Endpoints

### Upload API Specification

```
POST /v1/specifications
```

Upload an OpenAPI/Swagger JSON file.

**Example:**
```bash
curl -X 'POST' \
  'http://localhost:8080/v1/specifications' \
  -H 'accept: application/json' \
  -F 'file=@path/to/your/swagger.json'
```

### Query Endpoint Details

```
GET /v1/endpoints/{endpoint_path}
```

Get detailed information about a specific API endpoint.

**Example:**
```bash
curl -X 'GET' \
  'http://localhost:8080/v1/endpoints/users' \
  -H 'accept: application/json'
```

### Ask the AI Assistant

```
POST /v1/assistant/query
```

Ask a natural language question about the API.

**Example:**
```bash
curl -X 'POST' \
  'http://localhost:8080/v1/assistant/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What endpoints are available for user management?"
}'
```

### Health Check

```
GET /v1/health
```

**Example:**
```bash
curl -X 'GET' \
  'http://localhost:8080/v1/health' \
  -H 'accept: application/json'
```

## Implementation Details

- Built with FastAPI for high-performance API endpoints
- Pydantic for data validation and settings management
- Langchain integration for AI-powered responses
- OpenAI's language models for natural language understanding

## Development

To run tests:

```bash
pytest
```

## License

[MIT License](LICENSE)