function src_plataforma(){
	
function verificar_resposta(indice)
{
    if (quiz_finalizado)
        return;

    respostas_respondidas++;

    if (indice == corretas[pergunta_atual])
    {
        respostas_corretas++;

        pontuacao += 100;

        ultima_resposta_correta = true;
    }
    else
    {
        ultima_resposta_correta = false;
    }


    // A cada 300 pontos sobe um nível
    nivel = 1 + floor(pontuacao / 300);


    // Limite de nível
    if (nivel > 5)
        nivel = 5;


    // Próxima pergunta
    pergunta_atual++;


    // Verifica fim do quiz
    if (pergunta_atual >= array_length(perguntas))
    {
        quiz_finalizado = true;
    }
	
	function desenhar_botao(x1, y1, x2, y2, texto)
{
    var mx = device_mouse_x_to_gui(0);
    var my = device_mouse_y_to_gui(0);

    var mouse_sobre =
        point_in_rectangle(
            mx,
            my,
            x1,
            y1,
            x2,
            y2
        );


    if (mouse_sobre)
        draw_set_color(cor_botao_hover);
    else
        draw_set_color(cor_botao);


    draw_roundrect(
        x1,
        y1,
        x2,
        y2,
        false
    );


    draw_set_color(c_white);

    draw_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        texto
    );
}
}
}