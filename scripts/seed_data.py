from app.core.db import SessionLocal
from app.models.author import Author
from app.models.book import Book


def run() -> None:
    db = SessionLocal()
    try:
        if db.query(Author).count() > 0:
            return
        author1 = Author(name="George Orwell", country="UK", birth_year=1903)
        author2 = Author(name="Jane Austen", country="UK", birth_year=1775)
        db.add_all([author1, author2])
        db.flush()
        db.add_all(
            [
                Book(title="1984", isbn="9780451524935", publication_year=1949, genre="Dystopian", page_count=328, author_id=author1.id),
                Book(title="Animal Farm", isbn="9780451526342", publication_year=1945, genre="Political Satire", page_count=112, author_id=author1.id),
                Book(title="Pride and Prejudice", isbn="9780141439518", publication_year=1813, genre="Romance", page_count=480, author_id=author2.id),
            ]
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
