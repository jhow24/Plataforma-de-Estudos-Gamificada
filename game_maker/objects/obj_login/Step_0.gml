// obj_login — evento Step.
var mx = device_mouse_x_to_gui(0);
var my = device_mouse_y_to_gui(0);
var click = mouse_check_button_pressed(mb_left);

if (keyboard_check_pressed(vk_backspace)) {
    var name_length = string_length(global.quiz_player_name);
    if (name_length > 0) {
        global.quiz_player_name = string_delete(global.quiz_player_name, name_length, 1);
    }
    keyboard_string = "";
} else {
    var typed = keyboard_string;
    if (string_length(typed) > 0) {
        var remaining = 24 - string_length(global.quiz_player_name);
        if (remaining > 0) {
            global.quiz_player_name += string_copy(typed, 1, remaining);
        }
        keyboard_string = "";
    }
}

var confirm_login = keyboard_check_pressed(vk_enter)
    || (click && mx >= 340 && mx <= 620 && my >= 480 && my <= 550);

if (confirm_login) {
    var clean_name = global.quiz_player_name;
    while (string_length(clean_name) > 0 && string_char_at(clean_name, 1) == " ") {
        clean_name = string_delete(clean_name, 1, 1);
    }
    while (string_length(clean_name) > 0
        && string_char_at(clean_name, string_length(clean_name)) == " ") {
        clean_name = string_delete(clean_name, string_length(clean_name), 1);
    }

    if (string_length(clean_name) >= 2) {
        global.quiz_player_name = clean_name;
        keyboard_string = "";
        room_goto(Rm_game);
    } else {
        global.quiz_login_message = "Digite pelo menos 2 caracteres para continuar.";
    }
}
