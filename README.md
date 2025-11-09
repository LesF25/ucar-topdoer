# Incident Management Service

## Overview

This repository contains a small FastAPI service for tracking incidents reported by operators, monitoring systems, or partners. It exposes endpoints to create incidents, list them with optional status filtering, and update their status. PostgreSQL stores the state; SQLAlchemy handles the ORM layer; migrations are managed through Alembic.

## Local Development (Docker)

```bash
docker-compose up --build
```

Visit:
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

From the Swagger UI you can create incidents, list them, and update status without needing a separate client.

## Running Tests

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

The test compose file starts a dedicated Postgres instance (`test_app`), builds the app image, and executes `pytest` inside the container. Once tests complete, containers shut down automatically due to the `--abort-on-container-exit` flag.
