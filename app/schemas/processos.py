from datetime import datetime

from pydantic import BaseModel


class ProcessoOut(BaseModel):
    id: int
    numero_cnj: str
    tribunal: str
    classe: str | None = None
    orgao_julgador: str | None = None
    data_ajuizamento: datetime | None = None


class ProcessoListResponse(BaseModel):
    items: list[ProcessoOut]
    limit: int
    offset: int
    total: int
