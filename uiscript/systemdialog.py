#favor manter essa linha
import uiscriptlocale

width = 210
height = 355
button_width = 180
button_start = 15
category_space = 10

window = {
	"name":"SystemDialog",
	"style":("float",),
	"x":SCREEN_WIDTH - width,
	"y":SCREEN_HEIGHT - height - 30,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"board_transparent",
			"height":height+100,
			"width":width,
			"x":0,
			"y":0,
			"children":
			(
				{
					"name":"game_option_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start,
					"text":uiscriptlocale.GAMEOPTION_TITLE,
					"width":button_width,
				},
				{
					"name":"exit_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space + 30,
					"text":"Fechar Jogo [Alt+F4]",
					"width":button_width,
				},
				{
					"name":"change_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space + 60,
					"text":"Trocar Personagem",
					"width":button_width,
				},
				{
					"name":"logout_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space + 90,
					"text":"Desconectar",
					"width":button_width,
				},
				{
					"name":"whisper_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space*2 + 120,
					"text":"Mensagem [Shift+Enter]",
					"width":button_width,
				},
				{
					"name":"guild_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space*2 + 150,
					"text":"Painel da Guild [Alt+G]",
					"width":button_width,
				},
				{
					"name":"boot_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space*2 + 180,
					"text":"Boot de Rodar [F5]",
					"width":button_width,
				},
				{
					"name":"messenger_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space*3 + 210,
					"text":"Lista de Contatos [Alt+M]",
					"width":button_width,
				},
				{
					"name":"inventory_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space*3 + 240,
					"text":"Inventário [I]",
					"width":button_width,
				},
				{
					"name":"character_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":0,
					"y":button_start + category_space*3 + 270,
					"text":"Personagem [C]",
					"width":button_width,
				},
			),
		},
	),
}