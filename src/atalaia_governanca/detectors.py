"""Detectores determinísticos de PII e de sinais de transparência (LAI).

Sem NER, sem LLM, sem serviços externos: apenas regex e palavras-chave locais.
"""

from __future__ import annotations

import re
import unicodedata

from atalaia_governanca.models import SinalLAI, SinalPII

# --- PII ---------------------------------------------------------------------

# CPF por padrão textual (sem validação de dígito verificador; a PoC prova fluxo).
_RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
_RE_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
# Telefone BR em formatos comuns, exigindo separador/parênteses para evitar
# colidir com CPF (sequências longas de dígitos).
_RE_TELEFONE = re.compile(
    r"(?<!\d)(?:\(\d{2}\)\s?|\d{2}[\s-])?\d{4,5}-\d{4}(?!\d)"
)
# Marcador explícito de nome/pessoa (ex.: "nome: Fulano", "pessoa: Beltrano").
_RE_NOME = re.compile(r"\b(?:nome|pessoa)\s*:\s*\S+", re.IGNORECASE)


def detectar_pii(texto: str) -> list[SinalPII]:
    """Detecta sinais de PII preservando a ordem de descoberta, sem repetição."""

    encontrados: list[SinalPII] = []

    def _add(sinal: SinalPII) -> None:
        if sinal not in encontrados:
            encontrados.append(sinal)

    if _RE_CPF.search(texto):
        _add(SinalPII.CPF)
    if _RE_EMAIL.search(texto):
        _add(SinalPII.EMAIL)
    if _RE_TELEFONE.search(texto):
        _add(SinalPII.TELEFONE)
    if _RE_NOME.search(texto):
        _add(SinalPII.NOME)

    return encontrados


# --- LAI ---------------------------------------------------------------------

# Taxonomia -> palavras-chave (em minúsculas e sem acento).
_TAXONOMIA_LAI: dict[SinalLAI, tuple[str, ...]] = {
    SinalLAI.GASTO_PUBLICO: (
        "gasto publico",
        "despesa publica",
        "valor total",
        "verba publica",
        "recurso publico",
        "orcamento",
    ),
    SinalLAI.CONTRATO: (
        "contrato",
        "contratacao",
        "licitacao",
        "pregao",
    ),
    SinalLAI.BENEFICIO_PUBLICO: (
        "beneficio publico",
        "beneficio social",
        "auxilio",
        "subsidio",
    ),
    SinalLAI.DECISAO_ADMINISTRATIVA: (
        "decisao administrativa",
        "ato administrativo",
        "portaria",
        "processo administrativo",
    ),
    SinalLAI.INTERESSE_COLETIVO: (
        "interesse coletivo",
        "interesse publico",
        "interesse da sociedade",
    ),
}


def _normalizar(texto: str) -> str:
    """Minúsculas e remoção de acentos para casamento de palavras-chave."""

    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.lower()


def _texto_metadados(metadados: dict) -> str:
    """Serializa valores de metadados em um texto buscável."""

    partes: list[str] = []
    for valor in metadados.values():
        if isinstance(valor, (list, tuple)):
            partes.extend(str(v) for v in valor)
        else:
            partes.append(str(valor))
    return " ".join(partes)


def _contem_palavra_chave(alvo: str, palavra: str) -> bool:
    """Casa a palavra-chave respeitando limites de palavra.

    Evita falsos positivos por substring (ex.: 'licitacao' dentro de
    'solicitacao'). Palavras-chave com múltiplos termos usam limites nas
    extremidades.
    """

    padrao = r"\b" + re.escape(palavra) + r"\b"
    return re.search(padrao, alvo) is not None


def detectar_lai(texto: str, metadados: dict | None = None) -> list[SinalLAI]:
    """Detecta sinais de transparência combinando texto e metadados."""

    metadados = metadados or {}
    alvo = _normalizar(texto + " " + _texto_metadados(metadados))

    encontrados: list[SinalLAI] = []
    for sinal, palavras in _TAXONOMIA_LAI.items():
        if any(_contem_palavra_chave(alvo, p) for p in palavras):
            encontrados.append(sinal)

    return encontrados
