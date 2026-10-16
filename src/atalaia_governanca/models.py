"""Modelos de entrada/saída, enums e carregamento de casos."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Recomendacao(str, Enum):
    """Recomendações de fluxo possíveis. Conjunto fechado (CHK-04)."""

    PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL = "PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL"
    REVISAR_DADOS_PESSOAIS = "REVISAR_DADOS_PESSOAIS"
    REVISAR_TRANSPARENCIA = "REVISAR_TRANSPARENCIA"
    ESCALAR_HUMANO = "ESCALAR_HUMANO"


class SinalPII(str, Enum):
    """Sinais mínimos de dado pessoal reconhecidos pela PoC."""

    CPF = "CPF"
    EMAIL = "EMAIL"
    TELEFONE = "TELEFONE"
    NOME = "NOME"


class SinalLAI(str, Enum):
    """Taxonomia mínima de sinais de interesse de transparência."""

    GASTO_PUBLICO = "GASTO_PUBLICO"
    CONTRATO = "CONTRATO"
    BENEFICIO_PUBLICO = "BENEFICIO_PUBLICO"
    DECISAO_ADMINISTRATIVA = "DECISAO_ADMINISTRATIVA"
    INTERESSE_COLETIVO = "INTERESSE_COLETIVO"


class CasoInvalidoError(ValueError):
    """Erro de entrada: caso ausente, malformado ou com campos faltando."""


_CAMPOS_OBRIGATORIOS = ("caso_id", "titulo", "descricao")


@dataclass
class Caso:
    """Caso sintético de entrada."""

    caso_id: str
    titulo: str
    descricao: str
    metadados: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Caso":
        if not isinstance(data, dict):
            raise CasoInvalidoError(
                "O caso deve ser um objeto JSON (dicionário)."
            )

        faltando = [c for c in _CAMPOS_OBRIGATORIOS if not data.get(c)]
        if faltando:
            raise CasoInvalidoError(
                "Campos obrigatórios ausentes ou vazios: "
                + ", ".join(faltando)
            )

        metadados = data.get("metadados", {})
        if metadados is None:
            metadados = {}
        if not isinstance(metadados, dict):
            raise CasoInvalidoError("O campo 'metadados' deve ser um objeto.")

        return cls(
            caso_id=str(data["caso_id"]),
            titulo=str(data["titulo"]),
            descricao=str(data["descricao"]),
            metadados=metadados,
        )


@dataclass
class Resultado:
    """Resultado estruturado de uma análise."""

    caso_id: str
    dados_pessoais_detectados: bool
    sinais_pii: list[str]
    interesse_transparencia_detectado: bool
    sinais_lai: list[str]
    recomendacao: str
    revisao_humana_obrigatoria: bool
    motivos: list[str]
    regras_acionadas: list[str]
    gov_adr: str | None = None

    def to_dict(self) -> dict:
        return {
            "caso_id": self.caso_id,
            "dados_pessoais_detectados": self.dados_pessoais_detectados,
            "sinais_pii": list(self.sinais_pii),
            "interesse_transparencia_detectado": self.interesse_transparencia_detectado,
            "sinais_lai": list(self.sinais_lai),
            "recomendacao": self.recomendacao,
            "revisao_humana_obrigatoria": self.revisao_humana_obrigatoria,
            "motivos": list(self.motivos),
            "regras_acionadas": list(self.regras_acionadas),
            "gov_adr": self.gov_adr,
        }


def carregar_caso(path: str | Path) -> Caso:
    """Carrega um caso de um arquivo JSON com tratamento de erro claro."""

    caminho = Path(path)
    if not caminho.exists():
        raise CasoInvalidoError(f"Arquivo não encontrado: {caminho}")

    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - erro de I/O raro
        raise CasoInvalidoError(f"Não foi possível ler o arquivo: {exc}") from exc

    try:
        data = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise CasoInvalidoError(
            f"JSON inválido em {caminho}: {exc.msg} (linha {exc.lineno}, "
            f"coluna {exc.colno})"
        ) from exc

    return Caso.from_dict(data)
