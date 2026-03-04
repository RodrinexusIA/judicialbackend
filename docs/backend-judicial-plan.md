# Plano de backend para coleta e cruzamento de dados judiciais

## Escopo e objetivos
- Coletar dados públicos de múltiplas fontes do Judiciário (PJe, e-SAJ, TRT, TJ, TRF, Diários Oficiais, portais de precatórios/RPV).
- Normalizar e deduplicar processos, precatórios/RPVs e ações coletivas.
- Permitir filtros por OAB, ente público (Estado/Município) e tipo de requisição.
- Exportar listas estruturadas (CSV/Excel) e oferecer API para consumo externo.

## Arquitetura sugerida
### 1) Camada de ingestão (conectores)
- Conectores por fonte (ex.: PJe, e-SAJ, eproc, portais de precatórios, diários oficiais).
- Tratamento de limitações:
  - Rate limit com filas e backoff exponencial.
  - Captcha/anti-bot: filas de revisão manual ou integrações específicas.
  - Normalização de formatos (HTML, PDF, JSON, XML).
- Observabilidade de coleta: métricas de sucesso, falhas e latência.

### 2) Camada de normalização e enriquecimento
- Parsing de peças e metadados com extração de campos-chave:
  - Número único do processo (CNJ), classe, assunto, partes, advogados (OAB), ente público.
  - Para precatórios/RPVs: natureza, valor, data, tribunal, ente devedor.
- Normalização de nomes (partes, entes) com dicionários e regras de equivalência.
- Deduplicação com chaves compostas (CNJ + tribunal + classe + partes).

### 3) Camada de relacionamento e cruzamento
- Modelagem de relacionamento:
  - Processo ↔ Precatório/RPV
  - Processo ↔ Ação coletiva
  - Parte ↔ Advogado/OAB ↔ Ente público
- Regras de matching flexíveis (fuzzy matching) para nomes inconsistentes.
- Log de confiança por match (score + explicação).

### 4) Armazenamento
- Banco relacional (PostgreSQL) para dados normalizados e relacionamentos.
- Data lake/objeto (S3/MinIO) para documentos brutos (PDF, HTML).
- Índices para busca: Elastic/OpenSearch ou PostgreSQL full-text.

### 5) API e exportação
- API REST/GraphQL para consultas e filtros.
- Endpoints de exportação (CSV/XLSX) com paginação/streaming.
- Autenticação e rate limit por cliente.

## Pontos críticos e mitigação
- **Fontes instáveis**: fallback com cache e espelhamento periódico.
- **Dados inconsistentes**: pipeline de normalização com validações e flags de qualidade.
- **Escalabilidade**: filas assíncronas (ex.: RabbitMQ/Redis) para ingestão e parsing.
- **Compliance**: armazenar somente dados públicos e garantir logs de origem.

## Próximos passos recomendados
1. Mapear fontes prioritárias (por tribunal e tipo de dado).
2. Criar protótipos de 1–2 conectores críticos.
3. Definir esquema de dados mínimo (processo, parte, OAB, precatório).
4. Implementar um pipeline de ingestão + normalização mínimo (MVP).
5. Validar com casos reais e iterar nos modelos de deduplicação.
