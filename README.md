# Book Metadata and Recommendation API

A coursework-ready RESTful API built with FastAPI, SQLAlchemy, Alembic, JWT auth, and pytest.

## Features

- Authentication (`/auth/register`, `/auth/login`)
- Authors CRUD (`/authors`)
- Books CRUD with filters (`/books?genre=&year=&author_id=`)
- Reviews CRUD with filters (`/reviews?book_id=&user_id=&rating=`)
- Analytics endpoints:
  - `/analytics/genre-trends`
  - `/analytics/rating-distribution`
  - `/analytics/recommendations/{user_id}`
- Unified success and error response envelope

## Tech Stack

- FastAPI
- PostgreSQL (production default via `DATABASE_URL`)
- SQLAlchemy + Alembic
- JWT (`python-jose`) + bcrypt (`passlib`)
- Pytest + FastAPI TestClient

## Project Structure

```text
app/
  api/            # routers and auth deps
  core/           # config, db, security, error/response helpers
  models/         # SQLAlchemy models
  repositories/   # DB access layer
  schemas/        # Pydantic schemas
  services/       # business logic
alembic/          # migrations
tests/            # integration tests
docs/             # api docs, report template, presentation material
scripts/          # seed or utility scripts
```

## Local Setup

1. Create virtual env and install:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment:

```bash
cp .env.example .env
# update DATABASE_URL/JWT_SECRET_KEY as needed
```

3. Run migrations:

```bash
alembic upgrade head
```

4. (Optional) Seed sample data:

```bash
python scripts/seed_data.py
```

5. Start app:

```bash
uvicorn app.main:app --reload
```

6. Open API docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Test

```bash
pytest -q
```

## API Documentation PDF

- See [`docs/api_documentation.pdf`](docs/api_documentation.pdf)
- Source markdown: [`docs/api_documentation.md`](docs/api_documentation.md)

## Deployment (Render)

- Create a PostgreSQL service and a Web service.
- Set env vars: `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Build command: `pip install -r requirements.txt`
- Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Coursework Deliverables Mapping

- Code repository + commit history: this repo
- API docs PDF: `docs/api_documentation.pdf`
- Technical report draft/template: `docs/technical_report_template.md`
- Oral slides outline/script: `docs/presentation_outline.md` and `docs/oral_exam_script.md`
