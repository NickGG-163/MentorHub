from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from mentorhub.api_schemas import ErrorEnvelope, ErrorInfo
from mentorhub.health_router import router_health
from mentorhub.goals_router import router_goals


app = FastAPI()
app.include_router(router_health)
app.include_router(router_goals)


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
