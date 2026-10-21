#!/usr/bin/env python3
"""Gera o notebook autocontido do Colab a partir da engine e do banco canônico."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "colab" / "quiz_ensino_medio.py"
BANK = ROOT / "data" / "questions.json"
NOTEBOOK = ROOT / "colab" / "quiz_ensino_medio.ipynb"

loader = '''_CAMINHO_BANCO = Path(__file__).resolve().parents[1] / "data" / "questions.json"
with _CAMINHO_BANCO.open(encoding="utf-8") as arquivo:
    BANCO_QUESTOES = json.load(arquivo)
'''
source = ENGINE.read_text(encoding="utf-8")
if loader not in source:
    raise RuntimeError("Não encontrei o carregador do banco no arquivo Python; notebook não foi atualizado.")
questions = json.loads(BANK.read_text(encoding="utf-8"))
bank_json = json.dumps(questions, ensure_ascii=False, indent=2)
if "'''" in bank_json:
    raise RuntimeError("O banco contém delimitador incompatível com a célula autocontida.")
embedded_bank = "BANCO_QUESTOES = json.loads(r'''\n" + bank_json + "\n''')\n"
engine_cell = source.replace(loader, embedded_bank, 1)

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Circuito do Conhecimento — Ensino Médio\n",
                "\n",
                "Jogo educativo com **100 questões em cinco níveis**, 20 perguntas por nível.\n",
                "Acerte para ganhar XP de avanço; são necessários **300 XP no nível atual** para liberar o próximo.\n",
                "Acertos concedem 100 XP, com bônus de 25 XP a cada três acertos consecutivos. Erros dão 20 XP de participação, sem contar para a meta.\n",
                "\n",
                "Execute a célula de código para carregar as funções e depois a célula final para iniciar a campanha.\n",
                "Digite A, B, C ou D. Se a meta ainda não for alcançada, você pode repetir o nível; respostas corretas já pontuadas não voltam a render XP de avanço."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": engine_cell.splitlines(keepends=True)
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["validar_banco()\n", "campanha()\n"]
        }
    ],
    "metadata": {
        "colab": {"name": "quiz_ensino_medio.ipynb", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}
NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Notebook gerado: {NOTEBOOK}")
print(f"Banco incorporado: {len(questions)} questões em cinco níveis")
