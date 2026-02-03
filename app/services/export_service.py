import io

import pandas as pd
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Processo


def export_processos(db: Session, format: str) -> StreamingResponse:
    rows = db.scalars(select(Processo)).all()
    data = [
        {
            "numero_cnj": r.numero_cnj,
            "tribunal": r.tribunal,
            "classe": r.classe,
            "orgao_julgador": r.orgao_julgador,
            "data_ajuizamento": r.data_ajuizamento,
        }
        for r in rows
    ]
    df = pd.DataFrame(data)

    if format == "csv":
        buf = io.StringIO()
        df.to_csv(buf, index=False)
        buf.seek(0)
        return StreamingResponse(
            iter([buf.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=processos.csv"},
        )

    bio = io.BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="processos")
    bio.seek(0)
    return StreamingResponse(
        bio,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=processos.xlsx"},
    )
