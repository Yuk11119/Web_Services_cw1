# API Documentation (Coursework Submission)

Base URL: `http://127.0.0.1:8000`

## Response Formats

Success:

```json
{
  "data": {},
  "meta": {}
}
```

Error:

```json
{
  "error_code": "STRING_CODE",
  "message": "Human readable message",
  "details": {}
}
```

## Auth

### POST /auth/register
- Request: `{ "email": "user@example.com", "password": "password123" }`
- Responses: `201`, `400`

### POST /auth/login
- Request: `{ "email": "user@example.com", "password": "password123" }`
- Responses: `200`, `401`
- Returns bearer token in `data.access_token`

## Authors CRUD

- `POST /authors`
- `GET /authors?page=1&size=10`
- `GET /authors/{author_id}`
- `PUT /authors/{author_id}`
- `DELETE /authors/{author_id}`

## Books CRUD

- `POST /books`
- `GET /books?page=1&size=10&genre=&year=&author_id=`
- `GET /books/{book_id}`
- `PUT /books/{book_id}`
- `DELETE /books/{book_id}`

## Reviews CRUD

- `POST /reviews`
- `GET /reviews?page=1&size=10&book_id=&user_id=&rating=`
- `PUT /reviews/{review_id}`
- `DELETE /reviews/{review_id}`

## Analytics

### GET /analytics/genre-trends?start_year=&end_year=
Returns book count and average rating grouped by genre.

### GET /analytics/rating-distribution
Returns histogram-style distribution for ratings 1-5.

### GET /analytics/recommendations/{user_id}?limit=5
Returns recommendation candidates by genre affinity and average ratings.

## Status Codes

- `200 OK`
- `201 Created`
- `204 No Content`
- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `409 Conflict`
- `422 Unprocessable Entity`
- `500 Internal Server Error`

## Authentication

Protected routes require:

`Authorization: Bearer <token>`
