#favor manter essa linha
import uiscriptlocale

width = 150
height = 102

window = {
	"name":"ThreeWayWarEnter",
	"x":SCREEN_WIDTH - width - 3,
	"y":150,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"thinboard",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"Titulo",
					"type":"text",
					"text":"Encruzilhada",
					"x":0,
					"y":10,
					"fontsize":"LARGE",
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"Portoes",
					"type":"text",
					"text":"A entrada será fechada",
					"x":0,
					"y":30,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"Tempo",
					"type":"text",
					"text":"",
					"x":0,
					"y":46,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"EnterButton",
					"type":"redbutton",
					"width":90,
					"x":0,
					"y":64,
					"horizontal_align":"center",
					"text":"Entrar",
				},
			),
		},
	),
}
