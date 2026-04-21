from pydantic import BaseModel


class Meta(BaseModel):
    page: int | None = None
    size: int | None = None
    total: int | None = None
