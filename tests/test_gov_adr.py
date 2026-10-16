"""Testes de geração de GOV-ADR (CHK-06)."""

from datetime import datetime

from atalaia_governanca.engine import analisar
from atalaia_governanca.gov_adr import gerar_gov_adr, proximo_numero, slugify
from atalaia_governanca.models import Caso


def _resultado_conflito():
    caso = Caso(
        caso_id="CASO-003",
        titulo="t",
        descricao="CPF 123.456.789-00 e contrato público",
    )
    return analisar(caso)


def test_slugify():
    assert slugify("CASO-003") == "caso-003"
    assert slugify("Ação Pública") == "acao-publica"


def test_proximo_numero_vazio(tmp_path):
    assert proximo_numero(tmp_path) == 1


def test_gera_arquivo_e_conteudo(tmp_path):
    resultado = _resultado_conflito()
    agora = datetime(2026, 1, 1, 12, 0, 0)
    caminho = gerar_gov_adr(resultado, tmp_path, agora=agora)

    assert caminho.exists()
    assert caminho.name == "GOV-ADR-0001--caso-003.md"

    texto = caminho.read_text(encoding="utf-8")
    assert "## Decisão humana\n\nPENDENTE" in texto
    assert "ESCALAR_HUMANO" in texto
    assert "R-CONFLITO" in texto
    assert "2026-01-01T12:00:00" in texto
    assert "Versão do motor: 0.1.0" in texto


def test_numeracao_incremental(tmp_path):
    r1 = _resultado_conflito()
    r2 = _resultado_conflito()
    gerar_gov_adr(r1, tmp_path)
    segundo = gerar_gov_adr(r2, tmp_path)
    assert segundo.name.startswith("GOV-ADR-0002--")


def test_resultado_recebe_caminho(tmp_path):
    resultado = _resultado_conflito()
    gerar_gov_adr(resultado, tmp_path)
    assert resultado.gov_adr is not None
    assert "GOV-ADR-0001" in resultado.gov_adr
