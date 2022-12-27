#favor manter essa linha
import uiscriptlocale

width = 500
height = 350

window = {
	"name":"PainelStaffWindow",
	"style":("movable", "float",),
	"x":0, "y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title": "Painel de Administração",
			"children":
			(
				{
					"name":"Button_Return",
					"type":"redbutton",
					"text":"Voltar",
					"width":97,
					"x": width - 130,
					"y": 8,
					"hide":1,
				},
				{
					"name":"TabControl",
					"type":"window",
					"width":130,
					"height":height-41,
					"x":width-130,
					"y":41,
					"children":
					(
						{
							"name":"vertical_separator",
							"type":"verticalseparator",
							"height":height - 45,
							"x":-6,
							"y":-3,
						},
						{
							"name":"Tab_Button_01",
							"type":"redbutton",
							"text":"Guerras",
							"width":119,
							"x":0,
							"y":0,
						},
						{
							"name":"Tab_Button_02",
							"type":"redbutton",
							"text":"Eventos",
							"width":119,
							"x":0,
							"y":30*1,
						},
						{
							"name":"Tab_Button_03",
							"type":"redbutton",
							"text":"Torneios",
							"width":119,
							"x":0,
							"y":30*2,
						},
						{
							"name":"Tab_Button_04",
							"type":"redbutton",
							"text":"Sistemas",
							"width":119,
							"x":0,
							"y":30*3,
						},
						{
							"name":"Tab_Button_05",
							"type":"redbutton",
							"text":"Punições",
							"width":119,
							"x":0,
							"y":30*4,
						},
						{
							"name":"Tab_Button_06",
							"type":"redbutton",
							"text":"Histórico de Guerras",
							"width":119,
							"x":0,
							"y":30*5,
						},
						{
							"name":"Tab_Button_07",
							"type":"redbutton",
							"text":"Histórico de Eventos",
							"width":119,
							"x":0,
							"y":30*6,
						},
						{
							"name":"Tab_Button_08",
							"type":"redbutton",
							"text":"Histórico de Torneios",
							"width":119,
							"x":0,
							"y":30*7,
						},
						{
							"name":"Tab_Button_09",
							"type":"redbutton",
							"text":"Histórico de Sistemas",
							"width":119,
							"x":0,
							"y":30*8,
						},
						{
							"name":"Tab_Button_10",
							"type":"redbutton",
							"text":"Histórico de Punições",
							"width":119,
							"x":0,
							"y":30*9,
						},
					),
				},
			),
		},
	),
}
