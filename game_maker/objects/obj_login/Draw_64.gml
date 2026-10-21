// obj_login — evento Draw GUI. Resolução de GUI: 960 x 720.
var bg = make_color_rgb(13, 21, 27);
var panel = make_color_rgb(25, 38, 43);
var panel2 = make_color_rgb(31, 48, 52);
var mint = make_color_rgb(119, 238, 194);
var lime = make_color_rgb(208, 245, 112);
var ivory = make_color_rgb(241, 243, 231);
var muted = make_color_rgb(158, 177, 176);
var coral = make_color_rgb(255, 151, 125);

draw_set_alpha(1);
draw_set_color(bg);
draw_rectangle(0, 0, 960, 720, false);

draw_set_color(mint);
draw_text(48, 28, "CIRCUITO DO CONHECIMENTO");
draw_set_color(muted);
draw_text(48, 54, "QUIZ GAMIFICADO · ENSINO MÉDIO");
draw_set_color(make_color_rgb(57, 77, 78));
draw_rectangle(48, 82, 912, 84, false);

draw_set_color(lime);
draw_text(72, 180, "ENTRADA DO JOGADOR");
draw_set_color(ivory);
draw_text(72, 232, "Qual nome vamos usar na sua jornada?");
draw_set_color(muted);
draw_text(72, 274, "Digite seu nome ou apelido. Pressione ENTER para continuar.");

draw_set_color(panel);
draw_rectangle(230, 350, 730, 415, false);
draw_set_color(ivory);
var shown_name = global.quiz_player_name;
if (string_length(shown_name) == 0) shown_name = "Digite seu nome...";
draw_text(252, 373, shown_name + ((current_time div 500) mod 2 == 0 ? "|" : ""));

draw_set_color(panel2);
draw_rectangle(340, 480, 620, 550, false);
draw_set_color(lime);
draw_text(425, 504, "ENTRAR NO JOGO");
draw_set_color(muted);
draw_text(72, 575, global.quiz_login_message);
draw_text(72, 610, "Use BACKSPACE para corrigir · máximo 24 caracteres");
draw_set_color(coral);
draw_text(72, 642, "Entrada por apelido local; não é uma conta com senha.");
