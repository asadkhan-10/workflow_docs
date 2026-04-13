# Workflow Docs API

A REST API that generates technical documentation for automation workflows using AI. Users can submit n8n/Make.com workflow JSON or plain English descriptions and receive structured markdown documentation, including an overview, step-by-step breakdown, and failure point analysis.

Live at: `http://3.110.219.116/`

---

## Tech Stack

- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL with SQLAlchemy 2.0 and Alembic migrations
- **AI:** Groq API (LLaMA 3.3 70B)
- **Auth:** JWT via python-jose
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions → Docker Hub → AWS EC2

---

## Features

- User registration and JWT authentication
- Create and manage workflows (plain English or JSON input)
- AI-powered documentation generation per workflow
- Full CRUD on workflow resources
- Persistent PostgreSQL storage with Docker volumes

---

## Project Structure

```
workflow-docs-api/
├── app/
│   ├── main.py           # App entry point, router registration
│   ├── models.py         # SQLAlchemy models (User, Workflow)
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── database.py       # DB engine and session setup
│   ├── config.py         # Environment variable management
│   ├── oauth2.py         # JWT token creation and verification
│   ├── utils.py          # Password hashing
│   ├── ai.py             # Groq API integration
│   └── routers/
│       ├── auth.py       # Login endpoint
│       ├── users.py      # User CRUD
│       └── workflows.py  # Workflow CRUD + doc generation
├── alembic/              # Database migrations
├── tests/                # pytest test suite
├── docker-compose-dev.yml
├── docker-compose-prod.yml
├── Dockerfile
└── .github/
    └── workflows/
        └── build_deploy.yml  # CI/CD pipeline
```

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Get JWT access token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Register a new user |
| GET | `/users/{id}` | Get user by ID |
| DELETE | `/users/{id}` | Delete own account |

### Workflows
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workflows/` | Create a workflow |
| GET | `/workflows/` | List all your workflows |
| GET | `/workflows/{id}` | Get a specific workflow |
| DELETE | `/workflows/{id}` | Delete a workflow |
| POST | `/workflows/{id}/generate-docs` | Generate AI documentation |

---

## Running Locally

### Prerequisites

- Docker and Docker Compose installed
- A [Groq API key](https://console.groq.com)

### Setup

1. Clone the repo:

```bash
git clone https://github.com/asadkhan-10/workflow_docs.git
cd workflow-docs-api
```

2. Create a `.env` file in the project root:

```env
database_hostname=postgres
database_port=5432
database_username=postgres
database_password=yourpassword
database_name=workflow_docs
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=30
groq_api_key=your_groq_api_key
```

3. Start the containers:

```bash
docker-compose -f docker-compose-dev.yml up -d
```

4. Run database migrations:

```bash
docker-compose -f docker-compose-dev.yml exec api alembic upgrade head
```

5. Visit the interactive docs at `http://localhost:8000/docs`

---

## Running Tests

```bash
pytest
```

Tests use a separate test database and cover user creation, authentication, and workflow CRUD operations.

---

## CI/CD Pipeline

Every push to `main` triggers the following GitHub Actions pipeline:

```
push to main
    → Run pytest against a fresh PostgreSQL service container
    → Build Docker image and push to Docker Hub
    → SSH into AWS EC2, pull latest image, restart containers, run migrations
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `DATABASE_PASSWORD` | PostgreSQL password (testing env) |
| `SECRET_KEY` | JWT secret key (testing env) |
| `GROQ_API_KEY` | Groq API key (testing env) |
| `DOCKERHUB_USERNAME` | Docker Hub username (testing env) |
| `DOCKERHUB_TOKEN` | Docker Hub access token (testing env) |
| `EC2_HOST` | EC2 public IP (production env) |
| `EC2_USERNAME` | EC2 SSH username (production env) |
| `EC2_SSH_KEY` | EC2 private key contents (production env) |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `database_hostname` | PostgreSQL host |
| `database_port` | PostgreSQL port |
| `database_username` | PostgreSQL username |
| `database_password` | PostgreSQL password |
| `database_name` | PostgreSQL database name |
| `secret_key` | JWT signing secret |
| `algorithm` | JWT algorithm (HS256) |
| `access_token_expire_minutes` | Token expiry duration |
| `groq_api_key` | Groq API key for LLM access |

---

## Author

**Asad Khan**.

- GitHub: [@asadkhn10](https://github.com/asadkhn10)
- LinkedIn: [ww.linkedin.com/in/asad-ali-khan-connect101]
