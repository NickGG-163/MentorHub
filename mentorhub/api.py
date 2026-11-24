from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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
