// Circuito do Conhecimento — evento Draw GUI de obj_quiz.
// Resolução lógica configurada no Create: 960 x 720.
var bg = make_color_rgb(13, 21, 27);
var panel = make_color_rgb(25, 38, 43);
var panel2 = make_color_rgb(31, 48, 52);
var line = make_color_rgb(57, 77, 78);
var mint = make_color_rgb(119, 238, 194);
var lime = make_color_rgb(208, 245, 112);
var ivory = make_color_rgb(241, 243, 231);
var muted = make_color_rgb(158, 177, 176);
var coral = make_color_rgb(255, 151, 125);

draw_set_font(Font_jogo);
draw_set_alpha(1);
draw_set_color(bg);
draw_rectangle(0, 0, 960, 720, false);

// Cabeçalho comum.
draw_set_color(mint);
draw_text(48, 28, "CIRCUITO DO CONHECIMENTO");
draw_set_color(muted);
draw_text(48, 54, "QUIZ GAMIFICADO · ENSINO MEDIO");
draw_set_color(line);
draw_rectangle(48, 82, 912, 84, false);

if (global.quiz_state == "menu") {
    draw_set_color(lime);
    draw_text(72, 193, "APRENDA. JOGUE. EVOLUA.");
    draw_set_color(ivory);
    draw_text(72, 248, "Seu próximo nível começa com uma pergunta.");
    draw_set_color(muted);
    draw_text_ext(72, 300, "100 questões de Ensino Médio em cinco níveis: ", 7, 780);
	draw_text_ext(72, 350, "Calouro, Explorador, Estrategista, Mestre e Lenda. Cada nível tem 20 perguntas.", 7, 780);
	draw_text_ext(72, 370, "Ganhe XP com acertos e alcance 300 XP para avançar.", 7, 780);
    draw_set_color(panel);
    draw_rectangle(340, 540, 620, 610, false);
    draw_set_color(lime);
    draw_text(416, 562, "COMEÇAR JORNADA");
    draw_set_color(muted);
    draw_text(332, 642, "Clique no botão ou pressione ENTER");
} else if (global.quiz_state == "pergunta" || global.quiz_state == "feedback") {
    var question_index = global.quiz_order[global.quiz_index];
    var q = global.quiz_questions[question_index];
    var total = array_length(global.quiz_order);
    var progress = (global.quiz_index + 1) / total;
    var stage_name = string_upper(global.quiz_level_names[global.quiz_level - 1]);

    draw_set_color(muted);
    draw_text(50, 105, "NÍVEL " + string(global.quiz_level) + " · " + stage_name + "     QUESTÃO " + string(global.quiz_index + 1) + " / " + string(total));
    draw_text(650, 105, "XP " + string(global.quiz_stage_xp) + "/300 · COMBO " + string(global.quiz_combo));
    draw_set_color(line);
    draw_rectangle(50, 130, 910, 138, false);
    draw_set_color(mint);
    draw_rectangle(50, 130, 50 + 860 * progress, 138, false);

    draw_set_color(lime);
    draw_text(65, 169, q.area + "  ·  " + q.difficulty);
    draw_set_color(ivory);
    draw_text_ext(65, 205, q.question, 8, 820);

    for (var i = 0; i < 4; i++) {
        var y1 = 326 + i * 62;
        var y2 = y1 + 52;
        draw_set_color(panel);
        draw_rectangle(95, y1, 865, y2, false);
        if (global.quiz_selected == i) {
            draw_set_color(mint);
            draw_rectangle(95, y1, 100, y2, false);
        }
        if (global.quiz_state == "feedback" && i == q.answer) {
            draw_set_color(make_color_rgb(44, 92, 71));
            draw_rectangle(95, y1, 865, y2, false);
        } else if (global.quiz_state == "feedback" && i == global.quiz_selected && !global.quiz_last_correct) {
            draw_set_color(make_color_rgb(105, 56, 53));
            draw_rectangle(95, y1, 865, y2, false);
        } else if (global.quiz_selected == i) {
            draw_set_color(panel2);
            draw_rectangle(100, y1 + 1, 864, y2 - 1, false);
        }
        draw_set_color(muted);
        draw_text(115, y1 + 15, chr(65 + i) + ")");
        draw_set_color(ivory);
        draw_text_ext(157, y1 + 14, q.options[i], 5, 675);
    }

    if (global.quiz_state == "feedback") {
        draw_set_color(global.quiz_last_correct ? mint : coral);
        draw_text_ext(96, 575, global.quiz_message, 5, 555);
        draw_set_color(muted);
        draw_text_ext(96, 605, q.explanation, 10, 555);
        draw_set_color(panel2);
        draw_rectangle(675, 600, 865, 665, false);
        draw_set_color(lime);
        draw_text(715, 623, (global.quiz_index + 1 >= total) ? "VER RESULTADO  →" : "CONTINUAR  ");
    } else {
        draw_set_color(panel2);
        draw_rectangle(690, 600, 865, 665, false);
        draw_set_color(global.quiz_selected >= 0 ? lime : muted);
        draw_text(713, 623, "CONFIRMAR  ");
        draw_set_color(muted);
        draw_text(96, 615, "Escolha uma alternativa. Teclas A e D também funcionam.");
    }
} else if (global.quiz_state == "resultado") {
    var total = array_length(global.quiz_order);
    var percent = round(100 * global.quiz_correct / total);
    var reached = global.quiz_stage_xp >= global.quiz_xp_target;
    var stage_name = global.quiz_level_names[global.quiz_level - 1];

    draw_set_color(lime);
    draw_text(72, 150, "RESULTADO DO NÍVEL " + string(global.quiz_level) + " · " + string_upper(stage_name));
    draw_set_color(ivory);
    draw_text(72, 218, reached ? "META ALCANÇADA" : "META AINDA NÃO ALCANÇADA");
    draw_set_color(mint);
    draw_text(72, 272, string(global.quiz_correct) + " / " + string(total) + " respostas corretas · " + string(percent) + "%");
    draw_set_color(ivory);
    draw_text(72, 324, "XP de avanço: " + string(global.quiz_stage_xp) + " / " + string(global.quiz_xp_target));
    draw_set_color(muted);
    draw_text(72, 365, "XP total da campanha: " + string(global.quiz_total_xp) + " · Melhor combo: " + string(global.quiz_best_combo));
    draw_text_ext(72, 410, "Acertos rendem XP de avanço; cada terceiro acerto seguido dá +25 XP. Erros rendem +20 XP de participação e não contam para liberar o próximo nível.", 6, 790);

    draw_set_color(panel);
    draw_rectangle(300, 570, 660, 635, false);
    draw_set_color(reached ? lime : coral);
    if (!reached) {
        draw_text(397, 592, "TENTAR DE NOVO");
    } else if (global.quiz_level < array_length(global.quiz_level_names)) {
        draw_text(350, 592, "AVANÇAR PARA " + string_upper(global.quiz_level_names[global.quiz_level]));
    } else {
        draw_text(367, 592, "NOVA CAMPANHA");
    }
}

draw_set_color(line);
draw_rectangle(48, 684, 912, 686, false);
draw_set_color(muted);
draw_text(48, 692, "PROTÓTIPO EDUCACIONAL · 100 QUESTÕES · 5 NÍVEIS");
draw_text(782, 692, "GML + PYTHON");
