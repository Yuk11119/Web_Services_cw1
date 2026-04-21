from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.authors import router as authors_router
from app.api.books import router as books_router
from app.api.reviews import router as reviews_router
from app.core.db import Base, engine
from app.core.exceptions import AppError
from app.core.responses import error_response, success_response

app = FastAPI(title="Book Metadata and Recommendation API", version="1.0.0")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.exception_handler(AppError)
def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content=error_response(exc.error_code, exc.message, exc.details))


@app.exception_handler(RequestValidationError)
def validation_error_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response("VALIDATION_ERROR", "Request validation failed", {"errors": exc.errors()}),
    )


@app.get("/")
def health():
    return success_response({"service": "ok"})


app.include_router(auth_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(reviews_router)
app.include_router(analytics_router)
