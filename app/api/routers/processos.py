from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas import ProcessoListResponse, ProcessoOut
from app.services.export_service import export_processos
from app.services.processos_service import list_processos

router = APIRouter()


@router.get("", response_model=ProcessoListResponse)
def list_processos_endpoint(
    tribunal: str | None = None,
    numero_cnj: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> ProcessoListResponse:
    rows, total = list_processos(
        db,
        tribunal=tribunal,
        numero_cnj=numero_cnj,
        limit=limit,
        offset=offset,
    )
    return ProcessoListResponse(
        items=[
            ProcessoOut(
                id=r.id,
                numero_cnj=r.numero_cnj,
                tribunal=r.tribunal,
                classe=r.classe,
                orgao_julgador=r.orgao_julgador,
                data_ajuizamento=r.data_ajuizamento,
            )
            for r in rows
        ],
        limit=limit,
        offset=offset,
        total=total,
    )


@router.get("/export")
def export_processos_endpoint(
    format: str = Query("csv", pattern="^(csv|xlsx)$"),
    db: Session = Depends(get_db),
):
    return export_processos(db, format)
