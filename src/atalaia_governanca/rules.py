"""Regras de decisão determinísticas.

Nunca produz decisão final (PUBLICAR/RESTRINGIR/ANONIMIZAR). Casos de conflito
(PII + transparência) sempre escalam para humano (fail-safe).
"""

from __future__ import annotations

from dataclasses import dataclass

from atalaia_governanca.models import Recomendacao, SinalLAI, SinalPII


@dataclass
class Decisao:
    recomendacao: Recomendacao
    motivos: list[str]
    regras_acionadas: list[str]
    revisao_humana_obrigatoria: bool


def decidir(
    sinais_pii: list[SinalPII], sinais_lai: list[SinalLAI]
) -> Decisao:
    """Aplica a tabela de decisão sobre os sinais detectados."""

    tem_pii = len(sinais_pii) > 0
    tem_lai = len(sinais_lai) > 0

    nomes_pii = ", ".join(s.value for s in sinais_pii)
    nomes_lai = ", ".join(s.value for s in sinais_lai)

    if tem_pii and tem_lai:
        return Decisao(
            recomendacao=Recomendacao.ESCALAR_HUMANO,
            motivos=[
                f"Há sinais de dado pessoal ({nomes_pii}).",
                f"Há sinal de interesse de transparência ({nomes_lai}).",
                "Conflito entre proteção de dados e transparência exige "
                "revisão humana; o motor não decide divulgação ou restrição.",
            ],
            regras_acionadas=["R-CONFLITO"],
            revisao_humana_obrigatoria=True,
        )

    if tem_pii:
        return Decisao(
            recomendacao=Recomendacao.REVISAR_DADOS_PESSOAIS,
            motivos=[f"Há sinais de dado pessoal ({nomes_pii})."],
            regras_acionadas=["R-PII"],
            revisao_humana_obrigatoria=True,
        )

    if tem_lai:
        return Decisao(
            recomendacao=Recomendacao.REVISAR_TRANSPARENCIA,
            motivos=[
                f"Há sinal de interesse de transparência ({nomes_lai})."
            ],
            regras_acionadas=["R-LAI"],
            revisao_humana_obrigatoria=False,
        )

    return Decisao(
        recomendacao=Recomendacao.PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL,
        motivos=[
            "Nenhum sinal de dado pessoal ou de interesse de transparência "
            "foi detectado."
        ],
        regras_acionadas=["R-NEUTRO"],
        revisao_humana_obrigatoria=False,
    )
