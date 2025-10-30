# OnboardPro

[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/onboardpro/ci.yml?branch=main)](https://github.com/your-org/onboardpro/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**OnboardPro is a modern, API-first platform designed to streamline and automate the employee onboarding experience, ensuring new hires are productive, engaged, and integrated from day one.**

This repository contains the backend service, built with FastAPI and PostgreSQL, that powers the entire OnboardPro ecosystem.

## Project Overview

In today's competitive talent market, a disjointed or manual onboarding process leads to poor new hire experiences, reduced productivity, and higher turnover. OnboardPro tackles this head-on by providing a centralized, automated system for HR teams, hiring managers, and new employees.

Our platform enables the creation of structured, repeatable onboarding plans, automates task assignments, and provides clear visibility into the progress of each new hire. Whether you're a small startup or a large enterprise, OnboardPro helps you deliver a world-class onboarding journey.

For a deep dive into the product vision, user personas, and functional requirements, please see the full [**Product Requirements Document (PRD)**](./docs/PRD.md).

## Key Features

OnboardPro is packed with features designed to make onboarding seamless and effective. Our development is guided by clear user stories and epics, as outlined in our PRD.

*   ✅ **Customizable Onboarding Templates (Epic OB-01):**
    *   Create, update, and manage reusable onboarding templates for different roles, departments, or locations.
    *   Define a sequence of tasks, including document signing, equipment provisioning, and introductory meetings.

*   ✅ **Automated Employee Onboarding Workflows (Epic OB-02):**
    *   Assign a template to a new hire to automatically generate a personalized onboarding plan.
    *   Track task completion and overall progress for each employee in real-time.

*   ✅ **Task Management & Notifications (Epic OB-03):**
    *   Assign tasks to new hires, managers, or other stakeholders (e.g., IT, HR).
    *   (Roadmap) Send automated email reminders for pending and overdue tasks.

*   ✅ **RESTful API for Extensibility:**
    *   A robust, well-documented API allows for integration with your existing HRIS, payroll, and IT systems.

## Architecture at a Glance

OnboardPro is built on a modern, decoupled architecture. The core of the system is a REST-first API powered by FastAPI, which serves as the single source of truth. This design allows for flexible integration with various frontends (web, mobile) and third-party services.

![Architecture Diagram](./docs/architecture.png)
*A high-level diagram illustrating the API-centric design of OnboardPro.*

## Tech Stack

*   **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Database:** [PostgreSQL](https://www.postgresql.org/)
*   **Data Validation:** [Pydantic](https://pydantic-docs.helpmanual.io/)
*   **Database Migrations:** [Alembic](https://alembic.sqlalchemy.org/en/latest/)
*   **Async Support:** [Uvicorn](https://www.uvicorn.org/) & [AsyncPG](https://github.com/MagicStack/asyncpg)
*   **Containerization:** [Docker](https://www.docker.com/) & Docker Compose

## Getting Started

Ready to run OnboardPro locally? Follow these steps to get your development environment set up.

### Prerequisites

*   Python 3.9+
*   [Poetry](https://python-poetry.org/docs/#installation) for dependency management
*   [Docker](https://www.docker.com/get-started/) and Docker Compose
*   A running PostgreSQL instance (or use the provided `docker-compose.yml`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/onboardpro.git
    cd onboardpro
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

### Environment Variables

The application uses environment variables for configuration.

1.  Copy the example file:
    ```bash
    cp .env.example .env
    ```

2.  Edit the `.env` file with your local settings. The most important variable is `DATABASE_URL`:
    ```ini
    # .env
    DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/onboardpro_db"
    SECRET_KEY="your-super-secret-key-for-jwt"
    ```

### Database Migration

With your database running and `.env` configured, apply the database schema using Alembic.

```bash
poetry run alembic upgrade head
```

## Running the App

### Development

For local development, run the app with Uvicorn. It will automatically reload on code changes.

```bash
poetry run uvicorn onboardpro.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive documentation (Swagger UI) can be found at `http://127.0.0.1:8000/docs`.

### Production

For production, we recommend using a process manager like Gunicorn with Uvicorn workers behind a reverse proxy like Nginx.

Alternatively, you can use the provided Docker setup:

```bash
# Build and run the services (API + Database)
docker-compose up --build
```

## API Reference

The OnboardPro API is the core of the platform.

### Authentication Note

Most endpoints are protected and require a `Bearer` token in the `Authorization` header. The token can be obtained via the `/auth/token` endpoint (not detailed here). For the examples below, we assume you have a valid token.

### Endpoints

Here are some of the core API endpoints. For a complete, interactive list, please visit the `/docs` endpoint when the app is running.

| Method | Path                               | Description                                     |
| :----- | :--------------------------------- | :---------------------------------------------- |
| `POST` | `/templates/`                      | Create a new onboarding template.               |
| `GET`  | `/templates/{template_id}`         | Retrieve a specific onboarding template by ID.  |
| `POST` | `/employees/`                      | Create a new employee and start their onboarding. |
| `GET`  | `/employees/{employee_id}/progress`| Get the onboarding progress for an employee.    |

---

#### **Create an Onboarding Template**

*   **Endpoint:** `POST /templates/`
*   **Sample Request:**

    ```json
    {
      "name": "Software Engineer Onboarding",
      "description": "Standard 90-day plan for new SWE hires.",
      "tasks": [
        { "title": "Sign NDA", "due_days": 1 },
        { "title": "Setup development environment", "due_days": 3 },
        { "title": "Meet with your mentor", "due_days": 5 }
      ]
    }
    ```

*   **Sample Response (201 Created):**

    ```json
    {
      "id": 1,
      "name": "Software Engineer Onboarding",
      "description": "Standard 90-day plan for new SWE hires.",
      "tasks": [
        { "id": 1, "title": "Sign NDA", "due_days": 1 },
        { "id": 2, "title": "Setup development environment", "due_days": 3 },
        { "id": 3, "title": "Meet with your mentor", "due_days": 5 }
      ]
    }
    ```

## Usage Examples

Here’s how you can interact with the API using common command-line tools.

#### **Create a New Employee (cURL)**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/employees/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "full_name": "Ada Lovelace",
    "email": "ada.lovelace@example.com",
    "start_date": "2024-09-01",
    "template_id": 1
  }'
```

#### **Create a New Employee (HTTPie)**

```bash
http POST http://127.0.0.1:8000/employees/ \
  "Authorization:Bearer YOUR_ACCESS_TOKEN" \
  full_name="Ada Lovelace" \
  email="ada.lovelace@example.com" \
  start_date="2024-09-01" \
  template_id:=1
```

## Contributing

We welcome contributions from the community! Whether it's a bug fix, a new feature, or documentation improvements, your help is appreciated.

Please read our [**CONTRIBUTING.md**](./CONTRIBUTING.md) guide for details on our code of conduct and the process for submitting pull requests.

## Roadmap

We have an exciting future planned for OnboardPro! Here are some of the high-level features on our roadmap:

*   **Q4 2024:**
    *   Integration with third-party HRIS platforms (e.g., Workday, BambooHR).
    *   Advanced analytics dashboard for tracking onboarding metrics.
*   **Q1 2025:**
    *   Native E-signature support for documents.
    *   Role-based access control (RBAC) for admins, managers, and employees.
*   **Beyond:**
    *   Mobile application for new hires.
    *   Customizable email notification templates.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Contact & Support

*   **Bug Reports & Feature Requests:** Please open an issue on our [GitHub Issues](https://github.com/your-org/onboardpro/issues) page.
*   **General Inquiries:** Email us at `contact@onboardpro.dev`.
*   **Community:** Join our Slack channel (link coming soon!).