"""Geração de GOV-ADR em Markdown com formato estável.

A decisão humana inicia sempre como PENDENTE. A geração é explícita (fora do
engine) para não misturar evidência com código.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from pathlib import Path

from atalaia_governanca import VERSAO_MOTOR
from atalaia_governanca.models import Resultado

_RE_NUMERO = re.compile(r"GOV-ADR-(\d{4})--")


def slugify(valor: str) -> str:
    """Converte um identificador em slug ASCII minúsculo com hífens."""

    sem_acento = unicodedata.normalize("NFKD", valor)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", sem_acento).strip("-").lower()
    return slug or "caso"


def proximo_numero(dir_decisoes: str | Path) -> int:
    """Retorna o próximo número sequencial de GOV-ADR no diretório."""

    diretorio = Path(dir_decisoes)
    if not diretorio.exists():
        return 1

    maior = 0
    for arquivo in diretorio.glob("GOV-ADR-*.md"):
        m = _RE_NUMERO.search(arquivo.name)
        if m:
            maior = max(maior, int(m.group(1)))
    return maior + 1


def _render(resultado: Resultado, numero: int, agora: datetime) -> str:
    pii = ", ".join(resultado.sinais_pii) or "(nenhum)"
    lai = ", ".join(resultado.sinais_lai) or "(nenhum)"
    regras = "\n".join(f"- {r}" for r in resultado.regras_acionadas) or "- (nenhuma)"
    motivos = "\n".join(f"- {m}" for m in resultado.motivos) or "- (nenhum)"
    revisao = (
        "Obrigatória" if resultado.revisao_humana_obrigatoria else "Não obrigatória"
    )

    return f"""# GOV-ADR-{numero:04d} -- {resultado.caso_id}

- Timestamp: {agora.isoformat(timespec="seconds")}
- Versão do motor: {VERSAO_MOTOR}

## Contexto

Análise automatizada do caso `{resultado.caso_id}` pela PoC 0.1 LGPD/LAI. Esta é uma
recomendação de fluxo de governança, não um parecer jurídico.

## Sinais encontrados

- PII: {pii}
- LAI: {lai}

## Recomendação do motor

{resultado.recomendacao}

## Regras acionadas

{regras}

## Necessidade de revisão humana

{revisao}

## Decisão humana

PENDENTE

## Evidências

{motivos}
"""


def gerar_gov_adr(
    resultado: Resultado,
    dir_decisoes: str | Path,
    agora: datetime | None = None,
) -> Path:
    """Gera o arquivo GOV-ADR e retorna seu caminho.

    `agora` é injetável para testes determinísticos.
    """

    diretorio = Path(dir_decisoes)
    diretorio.mkdir(parents=True, exist_ok=True)

    numero = proximo_numero(diretorio)
    agora = agora or datetime.now()
    slug = slugify(resultado.caso_id)

    conteudo = _render(resultado, numero, agora)
    caminho = diretorio / f"GOV-ADR-{numero:04d}--{slug}.md"
    caminho.write_text(conteudo, encoding="utf-8")

    resultado.gov_adr = str(caminho).replace("\\", "/")
    return caminho
