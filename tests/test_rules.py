"""Testes das regras de decisão (CHK-03, CHK-04, CHK-05)."""

from atalaia_governanca.models import Recomendacao, SinalLAI, SinalPII
from atalaia_governanca.rules import decidir


def test_conflito_escala_humano():
    d = decidir([SinalPII.CPF], [SinalLAI.GASTO_PUBLICO])
    assert d.recomendacao is Recomendacao.ESCALAR_HUMANO
    assert d.revisao_humana_obrigatoria is True
    assert "R-CONFLITO" in d.regras_acionadas


def test_apenas_pii():
    d = decidir([SinalPII.CPF], [])
    assert d.recomendacao is Recomendacao.REVISAR_DADOS_PESSOAIS
    assert d.revisao_humana_obrigatoria is True


def test_apenas_lai():
    d = decidir([], [SinalLAI.CONTRATO])
    assert d.recomendacao is Recomendacao.REVISAR_TRANSPARENCIA
    assert d.revisao_humana_obrigatoria is False


def test_neutro():
    d = decidir([], [])
    assert d.recomendacao is Recomendacao.PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL
    assert d.revisao_humana_obrigatoria is False


def test_motivos_nunca_vazios():
    for pii, lai in [
        ([SinalPII.CPF], [SinalLAI.CONTRATO]),
        ([SinalPII.CPF], []),
        ([], [SinalLAI.CONTRATO]),
        ([], []),
    ]:
        assert decidir(pii, lai).motivos


def test_nunca_decisao_final():
    valores = {r.value for r in Recomendacao}
    assert "PUBLICAR" not in valores
    assert "RESTRINGIR" not in valores
    assert "ANONIMIZAR" not in valores
