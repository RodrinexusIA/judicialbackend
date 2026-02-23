import time
from datetime import datetime, timezone
from typing import Any

import requests

from app.core.config import settings


class DataJudClient:
    def __init__(self, min_interval: float = 0.5):
        self.url = settings.DATAJUD_TJGO_URL
        self.headers = {
            "Authorization": f"APIKey {settings.DATAJUD_API_KEY}",
            "Content-Type": "application/json",
        }
        self.min_interval = min_interval
        self._last_request = 0.0

    def _rate_limit(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request = time.monotonic()

    def search_by_oab(self, oab: str, page: int = 0, size: int = 50, max_retries: int = 5) -> dict:
        query = {
            "from": page * size,
            "size": size,
            "query": {
                "query_string": {
                    "query": f"*(OAB {oab})* OR *{oab}*",
                    "default_operator": "AND",
                }
            },
        }
        return self._post(query, max_retries=max_retries)

    def search_by_query_string(
        self, query_string: str, page: int = 0, size: int = 50, max_retries: int = 5
    ) -> dict:
        query = {
            "from": page * size,
            "size": size,
            "query": {
                "query_string": {
                    "query": query_string,
                    "default_operator": "AND",
                }
            },
        }
        return self._post(query, max_retries=max_retries)

    def _post(self, payload: dict, max_retries: int) -> dict:
        delay = 1.0
        for _ in range(max_retries):
            self._rate_limit()
            resp = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
            if resp.status_code == 429:
                time.sleep(delay)
                delay = min(delay * 2, 30)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError("Rate limit persistente (429) no DataJud")


def parse_data_ajuizamento(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return None

    raw = value.strip()
    if not raw:
        return None

    try:
        if len(raw) == 10:
            return datetime.strptime(raw, "%Y-%m-%d")

        normalized = raw.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except ValueError:
        return None


def parse_processo_source(source: dict[str, Any]) -> dict[str, Any]:
    classe = source.get("classe") or {}
    orgao = source.get("orgaoJulgador") or {}
    tribunal = source.get("tribunal") or "TJGO"
    return {
        "numero_cnj": source.get("numeroProcesso"),
        "tribunal": str(tribunal),
        "classe": classe.get("nome"),
        "orgao_julgador": orgao.get("nome"),
        "data_ajuizamento": parse_data_ajuizamento(source.get("dataAjuizamento")),
        "raw_json": source,
    }
