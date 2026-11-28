import json
import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import RequestResponseEndpoint

from mentorhub.api_schemas import ErrorEnvelope, ErrorInfo
from mentorhub.goals.goals_router import router_goals
from mentorhub.health_router import router_health
from mentorhub.tasks.tasks_router import router_tasks
from mentorhub.users.users_router import router_users

app = FastAPI()
app.include_router(router_health)
app.include_router(router_goals)
app.include_router(router_tasks)
app.include_router(router_users)


class RequestJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname,
                           "event": record.getMessage(),
                           "request_id": getattr(record, "request_id", None),
                           "method": getattr(record, "method", None),
                           "path": getattr(record, "path", None),
                           "status_code": getattr(record, "status_code", None),
                           "duration_ms": getattr(record, "duration_ms", None)})


request_logger = logging.getLogger("mentorhub.http")

request_log_handler = logging.StreamHandler()
request_log_handler.setFormatter(RequestJsonFormatter())

request_logger.addHandler(request_log_handler)
request_logger.setLevel(logging.INFO)
request_logger.propagate = False


@app.middleware("http")
async def log_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
    request_id = str(uuid4())
    started_at = perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    duration_ms = (perf_counter() - started_at) * 1000
    request_logger.info("request_completed", extra={
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_ms": round(duration_ms, 2)})
    return response


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    error = ErrorInfo(code="validation_error", message="Некорректные данные",
                      details=jsonable_encoder(exc.errors()))
    payload = ErrorEnvelope(error=error)
    return JSONResponse(status_code=422, content=jsonable_encoder(payload))


@app.exception_handler(StarletteHTTPException)
def handle_http_error(request: Request, exc: StarletteHTTPException):
    code = "not_found" if exc.status_code == 404 else "http_error"
    error = ErrorInfo(code=code, message=str(exc.detail), details=[])
    payload = ErrorEnvelope(error=error)
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(payload))
