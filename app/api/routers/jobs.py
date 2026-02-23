from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas import JobCreateRequest, JobCreatedResponse, JobStatusResponse
from app.services.jobs_service import create_datajud_job, get_job

router = APIRouter()


@router.post("/datajud/processos", response_model=JobCreatedResponse)
def create_job_datajud_processos(
    payload: JobCreateRequest, db: Session = Depends(get_db)
) -> JobCreatedResponse:
    job = create_datajud_job(db, payload.model_dump(exclude_none=True))
    return JobCreatedResponse(id=job.id, status=job.status)


@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)) -> JobStatusResponse:
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    params = job.params or {}
    return JobStatusResponse(
        id=job.id,
        status=job.status,
        total_found=params.get("total_found"),
        total_saved=job.result_count,
        error_message=job.error,
    )
