#!/usr/bin/env python3
"""Engine de perguntas do Circuito do Conhecimento.

Use o pacote completo para executar este arquivo: o banco de perguntas fica em
../data/questions.json. O notebook .ipynb inclui uma cópia embutida do banco e é
a opção autocontida para abrir no Google Colab.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Callable, Optional

NIVEIS = ["Calouro", "Explorador", "Estrategista", "Mestre", "Lenda"]
XP_PARA_AVANCAR = 300
XP_POR_ACERTO = 100
BONUS_COMBO = 25
XP_PARTICIPACAO = 20
LETRAS = "ABCD"

_CAMINHO_BANCO = Path(__file__).resolve().parents[1] / "data" / "questions.json"
with _CAMINHO_BANCO.open(encoding="utf-8") as arquivo:
    BANCO_QUESTOES = json.load(arquivo)


def validar_banco(banco: Optional[list[dict]] = None) -> bool:
    """Confere estrutura, distribuição e gabaritos do banco de dados."""
    questoes = BANCO_QUESTOES if banco is None else banco
    if len(questoes) != 100:
        raise ValueError(f"O banco precisa ter 100 questões; recebeu {len(questoes)}.")
    for nivel in range(1, len(NIVEIS) + 1):
        deste_nivel = [q for q in questoes if q.get("nivel") == nivel]
        if len(deste_nivel) != 20:
            raise ValueError(f"O nível {nivel} precisa ter 20 questões; recebeu {len(deste_nivel)}.")
    ids = set()
    for q in questoes:
        if q.get("id") in ids:
            raise ValueError(f"ID de questão repetido: {q.get('id')}")
        ids.add(q.get("id"))
        if len(q.get("opcoes", [])) != 4 or q.get("resposta") not in range(4):
            raise ValueError(f"Alternativas ou gabarito inválido em {q.get('id')}.")
        if not q.get("explicacao", "").strip():
            raise ValueError(f"Falta explicação em {q.get('id')}.")
    return True


def pontos_da_resposta(correta: bool, combo: int = 0) -> int:
    """Acerto: 100 XP e +25 a cada terceiro acerto seguido; erro: 20 XP de
    participação, que não contam para avançar de nível.
    """
    if not correta:
        return XP_PARTICIPACAO
    return XP_POR_ACERTO + (BONUS_COMBO if combo > 0 and combo % 3 == 0 else 0)


def jogar(
    nivel: int = 1,
    quantidade: int = 20,
    assunto: Optional[str] = None,
    *,
    xp_nivel_inicial: int = 0,
    ids_pontuados: Optional[set[str]] = None,
    seed: Optional[int] = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    banco: Optional[list[dict]] = None,
) -> dict:
    """Executa uma tentativa de até 20 questões de um nível.

    xp_nivel_inicial e ids_pontuados permitem que campanha() preserve o avanço
    conquistado quando o jogador repete um nível. Uma questão correta só rende
    XP de avanço uma vez por nível; erros rendem apenas XP de participação.
    """
    if nivel not in range(1, len(NIVEIS) + 1):
        raise ValueError("O nível deve estar entre 1 e 5.")
    if not isinstance(quantidade, int) or quantidade < 1:
        raise ValueError("A quantidade de questões deve ser um inteiro positivo.")
    banco_ativo = BANCO_QUESTOES if banco is None else banco
    disponiveis = [q for q in banco_ativo if q.get("nivel") == nivel]
    if assunto:
        disponiveis = [q for q in disponiveis if q.get("materia", "").casefold() == assunto.casefold()]
    if not disponiveis:
        raise ValueError(f"Não há questões para o nível {nivel} e o assunto selecionado.")

    gerador = random.Random(seed)
    rodada = disponiveis.copy()
    gerador.shuffle(rodada)
    rodada = rodada[: min(quantidade, len(rodada))]
    ja_pontuadas = ids_pontuados if ids_pontuados is not None else set()

    xp_nivel = xp_nivel_inicial
    xp_total_tentativa = 0
    xp_participacao = 0
    acertos = 0
    combo = 0
    melhor_combo = 0

    output_fn(f"\nNÍVEL {nivel} — {NIVEIS[nivel - 1].upper()} | Meta: {XP_PARA_AVANCAR} XP de avanço")
    output_fn(f"Questões nesta tentativa: {len(rodada)}")

    for indice, questao in enumerate(rodada, start=1):
        output_fn(f"\n[{indice:02d}/{len(rodada):02d}] {questao['materia']} · {questao['dificuldade']}")
        output_fn(questao["pergunta"])
        for posicao, alternativa in enumerate(questao["opcoes"]):
            output_fn(f"  {LETRAS[posicao]}) {alternativa}")

        resposta = input_fn("Sua resposta (A–D): ").strip().upper()
        while resposta not in LETRAS:
            resposta = input_fn("Digite A, B, C ou D: ").strip().upper()
        acertou = LETRAS.index(resposta) == questao["resposta"]

        if acertou:
            acertos += 1
            combo += 1
            melhor_combo = max(melhor_combo, combo)
            if questao["id"] not in ja_pontuadas:
                pontos = pontos_da_resposta(True, combo)
                ja_pontuadas.add(questao["id"])
                xp_nivel += pontos
                xp_total_tentativa += pontos
                sufixo = f" (+{BONUS_COMBO} de combo)" if pontos > XP_POR_ACERTO else ""
                output_fn(f"Correto! +{pontos} XP de avanço{sufixo}.")
            else:
                output_fn("Correto! Esta questão já concedeu XP de avanço neste nível.")
        else:
            combo = 0
            pontos = pontos_da_resposta(False, combo)
            xp_participacao += pontos
            xp_total_tentativa += pontos
            correta = questao["opcoes"][questao["resposta"]]
            output_fn(f"Não foi dessa vez. A resposta correta é {LETRAS[questao['resposta']]}) {correta}.")
            output_fn(f"+{pontos} XP de participação; esses pontos não contam para a meta do nível.")

        output_fn(f"Explicação: {questao['explicacao']}")
        output_fn(f"Progresso do nível: {xp_nivel}/{XP_PARA_AVANCAR} XP | Combo: {combo}")

    meta_alcancada = xp_nivel >= XP_PARA_AVANCAR
    output_fn("\n— RESULTADO DA TENTATIVA —")
    output_fn(f"Nível: {NIVEIS[nivel - 1]} ({nivel}/{len(NIVEIS)})")
    output_fn(f"Acertos: {acertos}/{len(rodada)} | Melhor combo: {melhor_combo}")
    output_fn(f"XP de avanço acumulado no nível: {xp_nivel}/{XP_PARA_AVANCAR}")
    output_fn(f"XP de participação nesta tentativa: {xp_participacao}")
    output_fn("Meta alcançada: pode avançar." if meta_alcancada else "Meta ainda não alcançada: repita este nível para continuar acumulando XP de avanço.")

    return {
        "nivel": nivel,
        "nome_nivel": NIVEIS[nivel - 1],
        "acertos": acertos,
        "questoes": len(rodada),
        "melhor_combo": melhor_combo,
        "xp_nivel": xp_nivel,
        "xp_total_tentativa": xp_total_tentativa,
        "xp_participacao": xp_participacao,
        "meta_alcancada": meta_alcancada,
        "ids_pontuados": ja_pontuadas,
    }


def campanha(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    *,
    seed: Optional[int] = None,
    banco: Optional[list[dict]] = None,
) -> dict:
    """Executa a jornada Calouro → Lenda, oferecendo avanço ou repetição."""
    total_xp = 0
    niveis_concluidos = 0
    tentativas = 0
    banco_ativo = BANCO_QUESTOES if banco is None else banco

    for nivel in range(1, len(NIVEIS) + 1):
        xp_nivel = 0
        ids_pontuados: set[str] = set()
        while xp_nivel < XP_PARA_AVANCAR:
            tentativa_seed = None if seed is None else seed + nivel * 100 + tentativas
            resultado = jogar(
                nivel=nivel,
                quantidade=20,
                xp_nivel_inicial=xp_nivel,
                ids_pontuados=ids_pontuados,
                seed=tentativa_seed,
                input_fn=input_fn,
                output_fn=output_fn,
                banco=banco_ativo,
            )
            tentativas += 1
            total_xp += resultado["xp_total_tentativa"]
            xp_nivel = resultado["xp_nivel"]
            if xp_nivel < XP_PARA_AVANCAR:
                escolha = input_fn("Meta não alcançada. ENTER para tentar novamente neste nível ou digite SAIR para encerrar: ").strip().casefold()
                if escolha in {"sair", "s", "q", "parar"}:
                    output_fn("Campanha pausada.")
                    return {"concluida": False, "niveis_concluidos": niveis_concluidos, "total_xp": total_xp, "tentativas": tentativas}
                continue

        niveis_concluidos += 1
        if nivel < len(NIVEIS):
            escolha = input_fn(f"Meta alcançada! Avançar para {NIVEIS[nivel].upper()}? [S/n]: ").strip().casefold()
            if escolha in {"n", "não", "nao", "sair", "q"}:
                break

    concluida = niveis_concluidos == len(NIVEIS)
    if concluida:
        output_fn("\nJORNADA CONCLUÍDA — você chegou ao nível Lenda!")
    output_fn(f"XP total da campanha: {total_xp} | Níveis concluídos: {niveis_concluidos}/{len(NIVEIS)}")
    return {"concluida": concluida, "niveis_concluidos": niveis_concluidos, "total_xp": total_xp, "tentativas": tentativas}


if __name__ == "__main__":
    validar_banco()
    campanha()
