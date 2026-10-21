// Circuito do Conhecimento — evento Step de obj_quiz.
var mx = device_mouse_x_to_gui(0);
var my = device_mouse_y_to_gui(0);
var click = mouse_check_button_pressed(mb_left);
var enter = keyboard_check_pressed(vk_enter) || keyboard_check_pressed(vk_space);

if (global.quiz_state == "menu") {
    if ((click && mx >= 340 && mx <= 620 && my >= 540 && my <= 610) || enter) {
        global.quiz_level = 1;
        global.quiz_total_xp = 0;
        global.quiz_participation_xp = 0;
        quiz_start(true);
    }
} else if (global.quiz_state == "pergunta") {
    if (!global.quiz_answered) {
        if (click) {
            for (var i = 0; i < 4; i++) {
                var y1 = 326 + i * 62;
                if (mx >= 95 && mx <= 865 && my >= y1 && my <= y1 + 52) {
                    global.quiz_selected = i;
                }
            }
        }
        for (var i = 0; i < 4; i++) {
            if (keyboard_check_pressed(ord(chr(65 + i)))) global.quiz_selected = i;
        }
        if (global.quiz_selected >= 0 && ((click && mx >= 675 && mx <= 865 && my >= 600 && my <= 665) || enter)) {
            quiz_submit();
        }
    }
} else if (global.quiz_state == "feedback") {
    if ((click && mx >= 675 && mx <= 865 && my >= 600 && my <= 665) || enter) {
        global.quiz_index += 1;
        global.quiz_selected = -1;
        global.quiz_answered = false;
        if (global.quiz_index >= array_length(global.quiz_order)) {
            global.quiz_state = "resultado";
        } else {
            global.quiz_state = "pergunta";
        }
    }
} else if (global.quiz_state == "resultado") {
    if ((click && mx >= 300 && mx <= 660 && my >= 570 && my <= 635) || enter) {
        if (global.quiz_stage_xp >= global.quiz_xp_target) {
            if (global.quiz_level < array_length(global.quiz_level_names)) {
                global.quiz_level += 1;
                quiz_start(true);
            } else {
                // Campanha completa: iniciar uma nova jornada do Calouro.
                global.quiz_level = 1;
                global.quiz_total_xp = 0;
                global.quiz_participation_xp = 0;
                quiz_start(true);
            }
        } else {
            // Tenta novamente no mesmo nível, preservando o XP já conquistado.
            quiz_start(false);
        }
    }
}
