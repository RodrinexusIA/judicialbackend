from pydantic import BaseModel, model_validator


class JobCreateRequest(BaseModel):
    oab: str | None = None
    query_string: str | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "JobCreateRequest":
        self.oab = self._normalize_str(self.oab)
        self.query_string = self._normalize_str(self.query_string)

        if not self.oab and not self.query_string:
            raise ValueError("Pelo menos um dos campos 'oab' ou 'query_string' é obrigatório")
        return self

    @staticmethod
    def _normalize_str(value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("Strings não podem ser vazias")
        return normalized


class JobCreatedResponse(BaseModel):
    id: str
    status: str


class JobStatusResponse(BaseModel):
    id: str
    status: str
    total_found: int | None = None
    total_saved: int | None = None
    error_message: str | None = None
