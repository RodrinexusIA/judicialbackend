from app.connectors.datajud import parse_processo_source


def test_parse_processo_source_basic() -> None:
    source = {
        "numeroProcesso": "0001234-56.2024.8.09.0001",
        "tribunal": "TJGO",
        "classe": {"nome": "Ação"},
        "orgaoJulgador": {"nome": "Vara Cível"},
        "dataAjuizamento": "2024-01-10",
    }

    parsed = parse_processo_source(source)

    assert parsed["numero_cnj"] == "0001234-56.2024.8.09.0001"
    assert parsed["tribunal"] == "TJGO"
    assert parsed["classe"] == "Ação"
    assert parsed["orgao_julgador"] == "Vara Cível"
    assert parsed["data_ajuizamento"] == "2024-01-10"
    assert parsed["raw_json"] == source
