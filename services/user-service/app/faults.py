import asyncio
import random
from dataclasses import asdict, dataclass

from fastapi import HTTPException


@dataclass
class FaultState:
    latency_ms: int = 0
    error_rate: float = 0.0  # 0.0 a 1.0 (probabilidade de retornar HTTP 500)

    def as_dict(self) -> dict:
        return asdict(self)


state = FaultState()


async def apply_faults() -> None:
    """Dependência do FastAPI executada antes dos endpoints funcionais."""
    if state.latency_ms > 0:
        # asyncio.sleep NÃO bloqueia o servidor; time.sleep bloquearia
        await asyncio.sleep(state.latency_ms / 1000)
    if state.error_rate > 0 and random.random() < state.error_rate:
        raise HTTPException(status_code=500, detail="injected fault")
