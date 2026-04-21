from pydantic import BaseModel


class GenreTrendItem(BaseModel):
    genre: str | None
    book_count: int
    avg_rating: float | None


class RatingDistributionItem(BaseModel):
    rating: int
    count: int


class RecommendationItem(BaseModel):
    book_id: int
    title: str
    genre: str | None
    score: float
