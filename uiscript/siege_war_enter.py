#favor manter essa linha
import uiscriptlocale

width = 145
height = 80

window = {
	"name":"SiegeWarEnter",
	"x":SCREEN_WIDTH - width - 3,
	"y":140,
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
				{"name":"","type":"text","text":"Guerra das Tochas","x":0,"y":10,"fontsize":"LARGE","horizontal_align":"center","text_horizontal_align":"center",},
				{"name":"Empire","type":"text","text":"Defensor: Jinno","x":0,"y":25,"horizontal_align":"center","text_horizontal_align":"center",},
				{
					"name":"EnterButton",
					"type":"redbutton",
					"width":90,
					"x":0,
					"y":40,
					"horizontal_align":"center",
					"text":"Entrar",
				},
			),
		},
	),
}
