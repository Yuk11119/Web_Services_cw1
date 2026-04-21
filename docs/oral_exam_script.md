# Oral Exam Script (Draft)

## Opening
This project is a book metadata and recommendation analytics API. It provides secure CRUD operations and analytics endpoints with consistent JSON API contracts.

## Architecture
The code follows a layered design: API routers call service layer business logic, which uses repository abstractions for persistence. This structure improves maintainability and testability.

## Demo Flow
1. Register and login to obtain JWT.
2. Create author and book, then query with filters.
3. Create review and show validation/error behavior.
4. Call analytics endpoints and explain output.

## Testing and Deployment
I implemented integration tests for auth, CRUD, validation, conflict handling, and analytics. The app is deployable to Render with PostgreSQL and Alembic migrations.

## GenAI Reflection
I used GenAI for planning, API contract iteration, and test scenario brainstorming, then manually validated schema, status codes, and business logic.
