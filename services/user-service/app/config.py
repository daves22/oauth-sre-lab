import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    service_name: str
    log_level: str
    startup_delay_seconds: float
    fault_latency_ms: int
    fault_error_rate: float


def load_settings() -> Settings:
    return Settings(
        service_name=os.getenv("SERVICE_NAME", "user-service"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        # Simula um serviço que demora a ficar pronto (útil p/ estudar readiness)
        startup_delay_seconds=float(os.getenv("STARTUP_DELAY_SECONDS", "0")),
        # Falhas iniciais; também podem ser alteradas em runtime via /admin/faults
        fault_latency_ms=int(os.getenv("FAULT_LATENCY_MS", "0")),
        fault_error_rate=float(os.getenv("FAULT_ERROR_RATE", "0")),
    )
