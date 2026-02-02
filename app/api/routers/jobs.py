from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.jobs_service import create_datajud_job, get_job

router = APIRouter()


@router.post("/datajud/processos")
def create_job_datajud_processos(payload: dict, db: Session = Depends(get_db)) -> dict:
    job = create_datajud_job(db, payload)
    return {"job_id": job.id, "status": job.status}


@router.get("/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)) -> dict:
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return {
        "id": job.id,
        "type": job.type,
        "status": job.status,
        "params": job.params,
        "result_count": job.result_count,
        "error": job.error,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }
