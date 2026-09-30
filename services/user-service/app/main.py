import logging
import time
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app import faults
from app.config import load_settings
from app.faults import apply_faults
from app.logging_config import setup_logging

settings = load_settings()
setup_logging(settings.service_name, settings.log_level)
logger = logging.getLogger("app")

faults.state.latency_ms = settings.fault_latency_ms
faults.state.error_rate = settings.fault_error_rate

STARTED_AT = time.monotonic()

# "Banco de dados" em memória por enquanto. Trocaremos por PostgreSQL depois.
USERS = {
    1: {"id": 1, "name": "Ana Souza", "email": "ana@example.com"},
    2: {"id": 2, "name": "Bruno Lima", "email": "bruno@example.com"},
    3: {"id": 3, "name": "Carla Dias", "email": "carla@example.com"},
}

app = FastAPI(title="User Service")


# --------------------------------------------------------------------------
# Middleware: request ID, duração, access log e tratamento de erros inesperados
# --------------------------------------------------------------------------
@app.middleware("http")
async def observe_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request.state.request_id = request_id
    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "unhandled exception",
            extra={"request_id": request_id, "endpoint": request.url.path},
        )
        response = JSONResponse(
            status_code=500,
            content={"error": "internal_error", "request_id": request_id},
        )

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["x-request-id"] = request_id

    # Health checks são frequentes e geram ruído: vão para DEBUG
    if request.url.path.startswith("/health"):
        level = logging.DEBUG
    elif response.status_code >= 500:
        level = logging.ERROR
    else:
        level = logging.INFO

    logger.log(
        level,
        "request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "endpoint": request.url.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


# --------------------------------------------------------------------------
# Health checks
# --------------------------------------------------------------------------
@app.get("/health/live")
def live():
    """Liveness: o processo está vivo?"""
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    """Readiness: está pronto para receber tráfego?"""
    if time.monotonic() - STARTED_AT < settings.startup_delay_seconds:
        return JSONResponse(status_code=503, content={"status": "not_ready"})
    return {"status": "ready"}


# --------------------------------------------------------------------------
# Endpoints funcionais (sujeitos às falhas injetadas)
# --------------------------------------------------------------------------
@app.get("/users", dependencies=[Depends(apply_faults)])
def list_users():
    return list(USERS.values())


@app.get("/users/{user_id}", dependencies=[Depends(apply_faults)])
def get_user(user_id: int):
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


# --------------------------------------------------------------------------
# Administração de falhas (SOMENTE laboratório: em produção exigiria proteção)
# --------------------------------------------------------------------------
class FaultConfig(BaseModel):
    latency_ms: int = Field(0, ge=0, le=60000)
    error_rate: float = Field(0.0, ge=0.0, le=1.0)


@app.get("/admin/faults")
def get_faults():
    return faults.state.as_dict()


@app.put("/admin/faults")
def set_faults(config: FaultConfig):
    faults.state.latency_ms = config.latency_ms
    faults.state.error_rate = config.error_rate
    logger.warning("faults updated", extra=faults.state.as_dict())
    return faults.state.as_dict()


@app.delete("/admin/faults")
def reset_faults():
    faults.state.latency_ms = 0
    faults.state.error_rate = 0.0
    logger.warning("faults reset")
    return faults.state.as_dict()
