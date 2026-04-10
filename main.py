import time

from fastapi import FastAPI, Request

from prometheus_client import Counter, Histogram, make_asgi_app

from core.config import get_settings
from schemas import RootResponse, HealthResponse
from routers import users

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(users.router)

REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    path = request.url.path
    REQUEST_COUNT.labels(
        request.method,
        path,
        str(response.status_code)
    ).inc()
    REQUEST_LATENCY.labels(
        request.method,
        path
    ).observe(duration)

    return response


@app.get("/", response_model=RootResponse)
def read_root():
    return {
        "message": f"Hello {settings.APP_NAME}",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "env": settings.ENV,
        "token_loaded": bool(settings.API_TOKEN)
    }