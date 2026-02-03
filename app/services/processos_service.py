from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Processo


def list_processos(
    db: Session,
    tribunal: str | None = None,
    numero_cnj: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Processo]:
    stmt = select(Processo).offset(offset).limit(limit)
    if tribunal:
        stmt = stmt.where(Processo.tribunal == tribunal)
    if numero_cnj:
        stmt = stmt.where(Processo.numero_cnj == numero_cnj)
    return db.scalars(stmt).all()
