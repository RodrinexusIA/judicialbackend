from datetime import datetime

from sqlalchemy import DateTime, Index, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Processo(Base):
    __tablename__ = "processos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numero_cnj: Mapped[str] = mapped_column(String, index=True)
    tribunal: Mapped[str] = mapped_column(String, index=True)
    classe: Mapped[str | None] = mapped_column(String, nullable=True)
    orgao_julgador: Mapped[str | None] = mapped_column(String, nullable=True)
    data_ajuizamento: Mapped[str | None] = mapped_column(String, nullable=True)

    raw_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


Index("ix_processos_numero_tribunal", Processo.numero_cnj, Processo.tribunal, unique=False)
