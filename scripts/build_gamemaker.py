#!/usr/bin/env python3
"""Gera o banco GML do GameMaker a partir de data/questions.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "questions.json"
OUTPUT = ROOT / "gamemaker" / "obj_quiz" / "Create_0.gml"


def gml_string(value: str) -> str:
    """Escapa uma string JSON como literal de texto GML."""
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    value = value.replace("\r", "\\r").replace("\n", "\\n")
    return f'"{value}"'


questions = json.loads(BANK.read_text(encoding="utf-8"))
if len(questions) != 100 or any(sum(q["nivel"] == n for q in questions) != 20 for n in range(1, 6)):
    raise ValueError("O banco precisa conter 20 questões em cada um dos cinco níveis.")

items = []
for q in questions:
    options = ", ".join(gml_string(option) for option in q["opcoes"])
    items.append(
        "    { id: " + gml_string(q["id"])
        + f", stage: {q['nivel']}"
        + ", area: " + gml_string(q["materia"].upper())
        + ", difficulty: " + gml_string(q["dificuldade"].upper())
        + ", question: " + gml_string(q["pergunta"])
        + f", options: [{options}], answer: {q['resposta']}, explanation: "
        + gml_string(q["explicacao"]) + " }"
    )

source = r'''// Circuito do Conhecimento — GameMaker Studio 2 / GML 2.3+
// Cole este conteúdo no evento Create do objeto obj_quiz.
// O banco de 100 questões é gerado a partir de data/questions.json.

display_set_gui_size(960, 720);
randomize();

global.quiz_state = "menu"; // menu, pergunta, feedback, resultado
global.quiz_level = 1;
global.quiz_level_names = ["Calouro", "Explorador", "Estrategista", "Mestre", "Lenda"];
global.quiz_xp_target = 300;
global.quiz_stage_xp = 0;
global.quiz_total_xp = 0;
global.quiz_participation_xp = 0;
global.quiz_attempt_xp = 0;
global.quiz_correct = 0;
global.quiz_combo = 0;
global.quiz_best_combo = 0;
global.quiz_index = 0;
global.quiz_selected = -1;
global.quiz_answered = false;
global.quiz_last_correct = false;
global.quiz_message = "";
global.quiz_explanation = "";
global.quiz_order = [];
global.quiz_rewarded_question_indices = [];
global.quiz_questions = [
__QUESTION_DATA__
];

quiz_start = function(_reset_stage_progress) {
    if (_reset_stage_progress) {
        global.quiz_stage_xp = 0;
        global.quiz_rewarded_question_indices = [];
    }
    global.quiz_attempt_xp = 0;
    global.quiz_correct = 0;
    global.quiz_combo = 0;
    global.quiz_best_combo = 0;
    global.quiz_index = 0;
    global.quiz_selected = -1;
    global.quiz_answered = false;
    global.quiz_message = "";
    global.quiz_explanation = "";
    global.quiz_order = [];

    for (var i = 0; i < array_length(global.quiz_questions); i++) {
        if (global.quiz_questions[i].stage == global.quiz_level) {
            array_push(global.quiz_order, i);
        }
    }
    // Fisher–Yates: 20 questões em ordem aleatória, sem repetição.
    for (var i = array_length(global.quiz_order) - 1; i > 0; i--) {
        var j = irandom(i);
        var temp = global.quiz_order[i];
        global.quiz_order[i] = global.quiz_order[j];
        global.quiz_order[j] = temp;
    }
    global.quiz_state = "pergunta";
};

quiz_submit = function() {
    if (global.quiz_selected < 0 || global.quiz_answered) return;
    var question_index = global.quiz_order[global.quiz_index];
    var q = global.quiz_questions[question_index];
    global.quiz_last_correct = (global.quiz_selected == q.answer);

    if (global.quiz_last_correct) {
        global.quiz_correct += 1;
        global.quiz_combo += 1;
        global.quiz_best_combo = max(global.quiz_best_combo, global.quiz_combo);
        var already_rewarded = false;
        for (var r = 0; r < array_length(global.quiz_rewarded_question_indices); r++) {
            if (global.quiz_rewarded_question_indices[r] == question_index) already_rewarded = true;
        }
        if (!already_rewarded) {
            var bonus = (global.quiz_combo mod 3 == 0) ? 25 : 0;
            var points = 100 + bonus;
            global.quiz_stage_xp += points;
            global.quiz_total_xp += points;
            global.quiz_attempt_xp += points;
            array_push(global.quiz_rewarded_question_indices, question_index);
            global.quiz_message = "Correto! +" + string(points) + " XP de avanço" + ((bonus > 0) ? " — bônus de combo!" : "");
        } else {
            global.quiz_message = "Correto! Esta questão já foi pontuada neste nível.";
        }
    } else {
        global.quiz_combo = 0;
        global.quiz_participation_xp += 20;
        global.quiz_total_xp += 20;
        global.quiz_attempt_xp += 20;
        global.quiz_message = "+20 XP de participação; a alternativa correta era " + chr(65 + q.answer) + ".";
    }

    global.quiz_explanation = q.explanation;
    global.quiz_answered = true;
    global.quiz_state = "feedback";
};
'''
source = source.replace("__QUESTION_DATA__", ",\n".join(items))
OUTPUT.write_text(source, encoding="utf-8")
print(f"GML atualizado: {OUTPUT}")
print(f"Questões exportadas: {len(questions)} (20 por nível)")
