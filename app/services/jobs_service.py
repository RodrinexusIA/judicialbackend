from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Job
from app.workers.tasks import collect_datajud_processos


def create_datajud_job(db: Session, params: dict) -> Job:
    job = Job(type="datajud_processos", status="queued", params=params)
    db.add(job)
    db.commit()
    db.refresh(job)

    collect_datajud_processos.delay(job.id)
    return job


def get_job(db: Session, job_id: str) -> Job | None:
    return db.scalar(select(Job).where(Job.id == job_id))
