import asyncio
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

import events_producer
import events_consumer


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await events_producer.connect()
    app.state.consumer_task = asyncio.create_task(events_consumer.consume())
    yield
    await events_producer.disconnect()
    app.state.consumer_task.cancel()


app = FastAPI(
    title="CinemaAbyss Events Service",
    description="Микросервис для обработки событий в системе CinemaAbyss",
    version="1.0.0",
    lifespan=lifespan,
)


class MovieEvent(BaseModel):
    movie_id: int
    title: str
    action: str
    user_id: int | None = None
    rating: float | None = None
    genres: list[str] | None = None
    description: str | None = None


class UserEvent(BaseModel):
    user_id: int
    username: str | None = None
    email: str | None = None
    action: str
    timestamp: datetime


class PaymentEvent(BaseModel):
    payment_id: int
    user_id: int
    amount: float
    status: str
    timestamp: datetime
    method_type: str | None = None


class EventResponse(BaseModel):
    status: str
    partition: int
    offset: int
    event: dict


class HealthResponse(BaseModel):
    status: bool


class Error(BaseModel):
    error: str


@app.get("/api/events/health", response_model=HealthResponse, tags=["health"])
async def get_events_service_health():
    """
    Проверка работоспособности микросервиса событий
    Возвращает статус работоспособности микросервиса событий
    """
    return HealthResponse(status=True)


@app.post(
    "/api/events/movie",
    response_model=EventResponse,
    tags=["events"],
    status_code=status.HTTP_201_CREATED,
)
async def create_movie_event(event: MovieEvent):
    """
    Создание события фильма
    Регистрирует новое событие, связанное с фильмом
    """

    result = await events_producer.send_movie_event(event.model_dump())

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return EventResponse(
        status=result["status"],
        partition=result["partition"],
        offset=result["offset"],
        event=result["event"],
    )


@app.post(
    "/api/events/user",
    response_model=EventResponse,
    tags=["events"],
    status_code=status.HTTP_201_CREATED,
)
async def create_user_event(event: UserEvent):
    """
    Создание события пользователя
    Регистрирует новое событие, связанное с пользователем
    """
    result = await events_producer.send_user_event(event.model_dump())

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return EventResponse(
        status=result["status"],
        partition=result["partition"],
        offset=result["offset"],
        event=result["event"],
    )


@app.post(
    "/api/events/payment",
    response_model=EventResponse,
    tags=["events"],
    status_code=status.HTTP_201_CREATED,
)
async def create_payment_event(event: PaymentEvent):
    """
    Создание события платежа
    Регистрирует новое событие, связанное с платежом
    """
    result = await events_producer.send_payment_event(event.model_dump())

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])

    return EventResponse(
        status=result["status"],
        partition=result["partition"],
        offset=result["offset"],
        event=result["event"],
    )
