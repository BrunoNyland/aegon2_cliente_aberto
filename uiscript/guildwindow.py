#favor manter essa linha
import uiscriptlocale

width = 500
height = 350

window = {
	"name":"GuildWindow",
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
			"title":uiscriptlocale.GUILD_NAME,
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
							"text":"Informações",
							"width":119,
							"x":0,
							"y":0,
						},
						{
							"name":"Tab_Button_02",
							"type":"redbutton",
							"text":"Mensagens",
							"width":119,
							"x":0,
							"y":30*1,
						},
						{
							"name":"Tab_Button_03",
							"type":"redbutton",
							"text":"Lista de Membros",
							"width":119,
							"x":0,
							"y":30*2,
						},
						{
							"name":"Tab_Button_04",
							"type":"redbutton",
							"text":"Habilidades",
							"width":119,
							"x":0,
							"y":30*3,
						},
						{
							"name":"Tab_Button_05",
							"type":"redbutton",
							"text":"Patentes",
							"width":119,
							"x":0,
							"y":30*4,
						},
						{
							"name":"Tab_Button_06",
							"type":"redbutton",
							"text":"Baú de Guild",
							"width":119,
							"x":0,
							"y":30*5,
						},
						{
							"name":"Tab_Button_07",
							"type":"redbutton",
							"text":"Ranking de Guild",
							"width":119,
							"x":0,
							"y":30*6,
						},
						{
							"name":"Tab_Button_08",
							"type":"redbutton",
							"text":"Histórico de War",
							"width":119,
							"x":0,
							"y":30*7,
						},
					),
				},
			),
		},
	),
}
