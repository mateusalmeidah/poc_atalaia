"""Testes de contrato de saída (CHK-04, CHK-05)."""

from atalaia_governanca.engine import analisar
from atalaia_governanca.models import Caso, Recomendacao

_VALIDAS = {r.value for r in Recomendacao}


def _analisar(descricao: str) -> dict:
    return analisar(Caso(caso_id="C", titulo="t", descricao=descricao)).to_dict()


def test_recomendacao_sempre_no_enum():
    for descricao in [
        "CPF 123.456.789-00",
        "contrato público",
        "CPF 123.456.789-00 e contrato público",
        "aviso neutro",
    ]:
        assert _analisar(descricao)["recomendacao"] in _VALIDAS


def test_sem_acoes_finais():
    proibidas = {"PUBLICAR", "RESTRINGIR", "ANONIMIZAR"}
    for descricao in ["CPF 123.456.789-00 e contrato público", "aviso neutro"]:
        assert _analisar(descricao)["recomendacao"] not in proibidas


def test_motivos_sempre_presentes():
    for descricao in ["CPF 123.456.789-00", "aviso neutro"]:
        assert _analisar(descricao)["motivos"]


def test_campos_do_contrato():
    saida = _analisar("CPF 123.456.789-00")
    esperados = {
        "caso_id",
        "dados_pessoais_detectados",
        "sinais_pii",
        "interesse_transparencia_detectado",
        "sinais_lai",
        "recomendacao",
        "revisao_humana_obrigatoria",
        "motivos",
        "regras_acionadas",
        "gov_adr",
    }
    assert esperados <= set(saida.keys())
