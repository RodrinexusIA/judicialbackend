# Judicial Backend MVP

Backend em Python para coleta e consulta de dados judiciais (DataJud TJGO), com FastAPI, Celery, PostgreSQL e Redis.

## Pré-requisitos
- Docker e Docker Compose

## Como rodar
1) Copie o arquivo de ambiente:
```bash
cp .env.example .env
```
2) Preencha `DATAJUD_API_KEY` no `.env`.
3) Suba os serviços:
```bash
docker-compose up --build
```
4) Acesse a documentação:
- Swagger: http://localhost:8000/docs

## Endpoints principais
### Criar job de coleta por OAB
```bash
curl -X POST http://localhost:8000/jobs/datajud/processos \
  -H "Content-Type: application/json" \
  -d '{"oab":"12345"}'
```

### Criar job de coleta por query_string (fallback)
```bash
curl -X POST http://localhost:8000/jobs/datajud/processos \
  -H "Content-Type: application/json" \
  -d '{"query_string":"OAB 12345"}'
```

### Consultar status do job
```bash
curl http://localhost:8000/jobs/<job_id>
```

### Consultar processos (paginado)
```bash
curl "http://localhost:8000/processos?limit=50&offset=0"
```

### Exportar processos
- CSV: http://localhost:8000/processos/export?format=csv
- XLSX: http://localhost:8000/processos/export?format=xlsx

## Estrutura do projeto
```
app/
  api/
  core/
  connectors/
  db/
  services/
  workers/
```

## Notas
- O conector DataJud aplica rate limit básico e backoff para erros 429.
- As tabelas são criadas automaticamente no startup do FastAPI. Para evoluir schema, use Alembic.

## Rodando testes
```bash
pytest
```
