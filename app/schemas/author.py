from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: str | None = Field(default=None, max_length=100)
    birth_year: int | None = Field(default=None, ge=0, le=2100)


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    country: str | None = Field(default=None, max_length=100)
    birth_year: int | None = Field(default=None, ge=0, le=2100)


class AuthorOut(BaseModel):
    id: int
    name: str
    country: str | None
    birth_year: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
