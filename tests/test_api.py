def test_auth_register_and_login(client):
    payload = {"email": "alice@example.com", "password": "password123"}
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 201
    assert res.json()["data"]["email"] == payload["email"]

    login = client.post("/auth/login", json=payload)
    assert login.status_code == 200
    assert "access_token" in login.json()["data"]


def test_auth_duplicate_email(client):
    payload = {"email": "dup@example.com", "password": "password123"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 400
    assert res.json()["error_code"] == "EMAIL_EXISTS"


def test_auth_required_for_protected_routes(client):
    res = client.get("/authors")
    assert res.status_code in {401, 403}


def test_author_book_review_crud_flow(client, auth_headers):
    author = client.post("/authors", json={"name": "Author A", "country": "UK", "birth_year": 1980}, headers=auth_headers)
    assert author.status_code == 201
    author_id = author.json()["data"]["id"]

    book = client.post(
        "/books",
        json={"title": "Book 1", "isbn": "1234567890123", "publication_year": 2020, "genre": "Sci-Fi", "page_count": 300, "author_id": author_id},
        headers=auth_headers,
    )
    assert book.status_code == 201
    book_id = book.json()["data"]["id"]

    list_books = client.get("/books?genre=Sci-Fi&page=1&size=10", headers=auth_headers)
    assert list_books.status_code == 200
    assert list_books.json()["meta"]["total"] == 1

    review = client.post("/reviews", json={"user_id": 1, "book_id": book_id, "rating": 5, "comment": "great"}, headers=auth_headers)
    assert review.status_code == 201
    review_id = review.json()["data"]["id"]

    update = client.put(f"/reviews/{review_id}", json={"rating": 4}, headers=auth_headers)
    assert update.status_code == 200
    assert update.json()["data"]["rating"] == 4

    delete_review = client.delete(f"/reviews/{review_id}", headers=auth_headers)
    assert delete_review.status_code == 204


def test_book_conflict_and_validation(client, auth_headers):
    author = client.post("/authors", json={"name": "Author B"}, headers=auth_headers)
    author_id = author.json()["data"]["id"]

    payload = {"title": "Book X", "isbn": "9999999999999", "publication_year": 2021, "genre": "Drama", "page_count": 120, "author_id": author_id}
    one = client.post("/books", json=payload, headers=auth_headers)
    assert one.status_code == 201

    duplicate = client.post("/books", json=payload, headers=auth_headers)
    assert duplicate.status_code == 409
    assert duplicate.json()["error_code"] == "ISBN_EXISTS"

    bad = client.post("/reviews", json={"user_id": 1, "book_id": one.json()["data"]["id"], "rating": 6}, headers=auth_headers)
    assert bad.status_code == 422


def test_analytics_endpoints(client, auth_headers):
    a1 = client.post("/authors", json={"name": "Author 1"}, headers=auth_headers).json()["data"]["id"]
    a2 = client.post("/authors", json={"name": "Author 2"}, headers=auth_headers).json()["data"]["id"]

    b1 = client.post("/books", json={"title": "D1", "isbn": "1111111111111", "publication_year": 2019, "genre": "Drama", "author_id": a1}, headers=auth_headers).json()["data"]["id"]
    b2 = client.post("/books", json={"title": "S1", "isbn": "2222222222222", "publication_year": 2022, "genre": "Sci-Fi", "author_id": a2}, headers=auth_headers).json()["data"]["id"]

    client.post("/reviews", json={"user_id": 1, "book_id": b1, "rating": 5, "comment": "nice"}, headers=auth_headers)
    client.post("/reviews", json={"user_id": 1, "book_id": b2, "rating": 3, "comment": "ok"}, headers=auth_headers)

    gt = client.get("/analytics/genre-trends?start_year=2010&end_year=2030", headers=auth_headers)
    assert gt.status_code == 200
    assert len(gt.json()["data"]) >= 1

    rd = client.get("/analytics/rating-distribution", headers=auth_headers)
    assert rd.status_code == 200
    ratings = [row["rating"] for row in rd.json()["data"]]
    assert 3 in ratings and 5 in ratings

    rec = client.get("/analytics/recommendations/1?limit=5", headers=auth_headers)
    assert rec.status_code == 200
    assert "data" in rec.json()
