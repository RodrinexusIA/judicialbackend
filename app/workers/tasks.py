from sqlalchemy import select

from app.connectors.datajud import DataJudClient, parse_processo_source
from app.db.models import Job, Processo
from app.db.session import SessionLocal
from app.workers.celery_app import celery


@celery.task(name="collect_datajud_processos")
def collect_datajud_processos(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.scalar(select(Job).where(Job.id == job_id))
        if not job:
            return

        job.status = "running"
        db.commit()

        params = job.params or {}
        oab = params.get("oab")
        query_string = params.get("query_string")
        if not oab and not query_string:
            job.status = "failed"
            job.error = "Parâmetro 'oab' ou 'query_string' é obrigatório"
            db.commit()
            return

        client = DataJudClient()
        total_saved = 0

        page = 0
        while True:
            if oab:
                data = client.search_by_oab(oab=oab, page=page, size=50)
            else:
                data = client.search_by_query_string(query_string=query_string, page=page, size=50)

            hits = data.get("hits", {}).get("hits", [])
            if not hits:
                break

            for hit in hits:
                src = hit.get("_source", {})
                parsed = parse_processo_source(src)
                if not parsed.get("numero_cnj"):
                    continue
                proc = Processo(**parsed)
                db.add(proc)
                total_saved += 1

            db.commit()
            page += 1

        job.status = "done"
        job.result_count = total_saved
        db.commit()

    except Exception as exc:
        job = db.scalar(select(Job).where(Job.id == job_id))
        if job:
            job.status = "failed"
            job.error = str(exc)
            db.commit()
    finally:
        db.close()
