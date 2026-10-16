"""Testes da CLI (Req 9 e Req 10)."""

import json
from pathlib import Path

from atalaia_governanca.cli import main

EXEMPLOS = Path(__file__).resolve().parent.parent / "examples"


def test_analyze_legivel(capsys):
    code = main(["analyze", str(EXEMPLOS / "caso_01.json")])
    out = capsys.readouterr().out
    assert code == 0
    assert "Recomendação: REVISAR_DADOS_PESSOAIS" in out


def test_analyze_json(capsys):
    code = main(["analyze", str(EXEMPLOS / "caso_03.json"), "--json"])
    out = capsys.readouterr().out
    assert code == 0
    data = json.loads(out)
    assert data["recomendacao"] == "ESCALAR_HUMANO"
    assert data["revisao_humana_obrigatoria"] is True


def test_analyze_gera_gov_adr(capsys, tmp_path):
    code = main(
        [
            "analyze",
            str(EXEMPLOS / "caso_03.json"),
            "--gov-adr",
            "--dir-decisoes",
            str(tmp_path),
        ]
    )
    out = capsys.readouterr().out
    assert code == 0
    assert "GOV-ADR:" in out
    assert list(tmp_path.glob("GOV-ADR-*.md"))


def test_arquivo_inexistente(capsys):
    code = main(["analyze", "nao_existe.json"])
    err = capsys.readouterr().err
    assert code != 0
    assert "não encontrado" in err.lower()


def test_json_invalido(tmp_path, capsys):
    ruim = tmp_path / "ruim.json"
    ruim.write_text("{ invalido", encoding="utf-8")
    code = main(["analyze", str(ruim)])
    err = capsys.readouterr().err
    assert code != 0
    assert "json inválido" in err.lower()


def test_campos_ausentes(tmp_path, capsys):
    incompleto = tmp_path / "incompleto.json"
    incompleto.write_text(json.dumps({"caso_id": "X"}), encoding="utf-8")
    code = main(["analyze", str(incompleto)])
    err = capsys.readouterr().err
    assert code != 0
    assert "obrigatórios" in err.lower()
