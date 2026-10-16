"""Testes de integração do motor com os casos mínimos CASO-001..004."""

from pathlib import Path

from atalaia_governanca.engine import analisar
from atalaia_governanca.models import Recomendacao, carregar_caso

EXEMPLOS = Path(__file__).resolve().parent.parent / "examples"


def _analisar(nome: str):
    return analisar(carregar_caso(EXEMPLOS / nome))


def test_caso_01_apenas_pii():
    r = _analisar("caso_01.json")
    assert r.dados_pessoais_detectados is True
    assert r.interesse_transparencia_detectado is False
    assert r.recomendacao == Recomendacao.REVISAR_DADOS_PESSOAIS.value
    assert r.revisao_humana_obrigatoria is True


def test_caso_02_apenas_transparencia():
    r = _analisar("caso_02.json")
    assert r.dados_pessoais_detectados is False
    assert r.interesse_transparencia_detectado is True
    assert r.recomendacao == Recomendacao.REVISAR_TRANSPARENCIA.value


def test_caso_03_conflito():
    r = _analisar("caso_03.json")
    assert r.dados_pessoais_detectados is True
    assert r.interesse_transparencia_detectado is True
    assert r.recomendacao == Recomendacao.ESCALAR_HUMANO.value
    assert r.revisao_humana_obrigatoria is True


def test_caso_04_neutro():
    r = _analisar("caso_04.json")
    assert r.dados_pessoais_detectados is False
    assert r.interesse_transparencia_detectado is False
    assert r.recomendacao == Recomendacao.PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL.value
    assert r.motivos  # saída auditável mesmo no caso neutro
