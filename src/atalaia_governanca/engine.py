"""Motor de orquestração: detectores + regras -> Resultado."""

from __future__ import annotations

from atalaia_governanca.detectors import detectar_lai, detectar_pii
from atalaia_governanca.models import Caso, Resultado
from atalaia_governanca.rules import decidir


def analisar(caso: Caso) -> Resultado:
    """Analisa um caso e retorna o resultado estruturado (sem gerar GOV-ADR)."""

    texto = f"{caso.titulo}\n{caso.descricao}"

    sinais_pii = detectar_pii(texto)
    sinais_lai = detectar_lai(texto, caso.metadados)

    decisao = decidir(sinais_pii, sinais_lai)

    return Resultado(
        caso_id=caso.caso_id,
        dados_pessoais_detectados=len(sinais_pii) > 0,
        sinais_pii=[s.value for s in sinais_pii],
        interesse_transparencia_detectado=len(sinais_lai) > 0,
        sinais_lai=[s.value for s in sinais_lai],
        recomendacao=decisao.recomendacao.value,
        revisao_humana_obrigatoria=decisao.revisao_humana_obrigatoria,
        motivos=decisao.motivos,
        regras_acionadas=decisao.regras_acionadas,
        gov_adr=None,
    )
