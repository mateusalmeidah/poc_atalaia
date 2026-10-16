"""PoC 0.1 - Motor determinístico de apoio à decisão LGPD/LAI (ATALAIA).

Camada de governança que detecta sinais de dado pessoal (PII) e de interesse de
transparência (LAI), produz uma recomendação de fluxo e escala conflitos para
revisão humana, registrando evidência em GOV-ADR.
"""

VERSAO_MOTOR = "0.1.0"

from atalaia_governanca.models import (  # noqa: E402
    Caso,
    CasoInvalidoError,
    Recomendacao,
    Resultado,
    SinalLAI,
    SinalPII,
    carregar_caso,
)
from atalaia_governanca.engine import analisar  # noqa: E402

__all__ = [
    "VERSAO_MOTOR",
    "Caso",
    "CasoInvalidoError",
    "Recomendacao",
    "Resultado",
    "SinalLAI",
    "SinalPII",
    "carregar_caso",
    "analisar",
]
