from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Processo


def list_processos(
    db: Session,
    tribunal: str | None = None,
    numero_cnj: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[Processo], int]:
    stmt = select(Processo)
    count_stmt = select(func.count()).select_from(Processo)

    if tribunal:
        stmt = stmt.where(Processo.tribunal == tribunal)
        count_stmt = count_stmt.where(Processo.tribunal == tribunal)
    if numero_cnj:
        stmt = stmt.where(Processo.numero_cnj == numero_cnj)
        count_stmt = count_stmt.where(Processo.numero_cnj == numero_cnj)

    stmt = stmt.order_by(Processo.id.asc()).offset(offset).limit(limit)
    rows = db.scalars(stmt).all()
    total = db.scalar(count_stmt) or 0
    return rows, total
