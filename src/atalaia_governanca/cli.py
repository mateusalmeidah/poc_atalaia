"""Interface de linha de comando da PoC.

Uso:
    python -m atalaia_governanca.cli analyze <arquivo.json> [--gov-adr] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from atalaia_governanca.engine import analisar
from atalaia_governanca.gov_adr import gerar_gov_adr
from atalaia_governanca.models import CasoInvalidoError, Resultado, carregar_caso

_DIR_DECISOES_PADRAO = "spec/decisoes"


def _formatar_legivel(resultado: Resultado) -> str:
    linhas = [
        f"Caso: {resultado.caso_id}",
        f"Dados pessoais detectados: {'sim' if resultado.dados_pessoais_detectados else 'não'}",
        f"Sinais PII: {', '.join(resultado.sinais_pii) or '(nenhum)'}",
        f"Interesse de transparência: {'sim' if resultado.interesse_transparencia_detectado else 'não'}",
        f"Sinais LAI: {', '.join(resultado.sinais_lai) or '(nenhum)'}",
        f"Recomendação: {resultado.recomendacao}",
        f"Revisão humana obrigatória: {'sim' if resultado.revisao_humana_obrigatoria else 'não'}",
        "Motivos:",
    ]
    linhas.extend(f"  - {m}" for m in resultado.motivos)
    if resultado.gov_adr:
        linhas.append(f"GOV-ADR: {resultado.gov_adr}")
    return "\n".join(linhas)


def _cmd_analyze(args: argparse.Namespace) -> int:
    try:
        caso = carregar_caso(args.arquivo)
    except CasoInvalidoError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2

    resultado = analisar(caso)

    if args.gov_adr:
        dir_decisoes = Path(args.dir_decisoes)
        gerar_gov_adr(resultado, dir_decisoes)

    if args.json:
        print(json.dumps(resultado.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_formatar_legivel(resultado))

    return 0


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atalaia-governanca",
        description="Motor determinístico de apoio à decisão LGPD/LAI (PoC 0.1).",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    p_analyze = sub.add_parser("analyze", help="Analisa um caso em JSON.")
    p_analyze.add_argument("arquivo", help="Caminho do caso em JSON.")
    p_analyze.add_argument(
        "--gov-adr",
        action="store_true",
        help="Gera o GOV-ADR correspondente.",
    )
    p_analyze.add_argument(
        "--json",
        action="store_true",
        help="Imprime a saída estruturada em JSON.",
    )
    p_analyze.add_argument(
        "--dir-decisoes",
        default=_DIR_DECISOES_PADRAO,
        help="Diretório de saída dos GOV-ADRs (padrão: spec/decisoes).",
    )
    p_analyze.set_defaults(func=_cmd_analyze)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
