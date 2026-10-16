"""Testes dos detectores de PII e LAI (CHK-01, CHK-02)."""

from atalaia_governanca.detectors import detectar_lai, detectar_pii
from atalaia_governanca.models import SinalLAI, SinalPII


def test_detecta_cpf():
    assert SinalPII.CPF in detectar_pii("CPF 123.456.789-00 informado")


def test_detecta_cpf_sem_pontuacao():
    assert SinalPII.CPF in detectar_pii("documento 12345678900")


def test_detecta_email():
    assert SinalPII.EMAIL in detectar_pii("contato fulano.ficticio@exemplo.test")


def test_detecta_telefone():
    assert SinalPII.TELEFONE in detectar_pii("ligar para (79) 99999-0000")


def test_detecta_nome_marcador():
    assert SinalPII.NOME in detectar_pii("nome: Fulano")


def test_pii_vazio_quando_neutro():
    assert detectar_pii("horário de funcionamento da biblioteca") == []


def test_pii_sem_duplicatas():
    texto = "e-mail a@b.test e também c@d.test"
    sinais = detectar_pii(texto)
    assert sinais.count(SinalPII.EMAIL) == 1


def test_detecta_lai_gasto_publico():
    assert SinalLAI.GASTO_PUBLICO in detectar_lai("valor total do orçamento", {})


def test_detecta_lai_contrato():
    assert SinalLAI.CONTRATO in detectar_lai("processo de licitação", {})


def test_detecta_lai_por_metadados():
    sinais = detectar_lai("texto neutro", {"categoria": "beneficio publico"})
    assert SinalLAI.BENEFICIO_PUBLICO in sinais


def test_lai_ignora_acentuacao():
    assert SinalLAI.GASTO_PUBLICO in detectar_lai("despesa pública alta", {})


def test_lai_vazio_quando_neutro():
    assert detectar_lai("novo horário da biblioteca", {}) == []


def test_lai_sem_duplicatas():
    texto = "contrato e contratação e licitação"
    sinais = detectar_lai(texto, {})
    assert sinais.count(SinalLAI.CONTRATO) == 1
