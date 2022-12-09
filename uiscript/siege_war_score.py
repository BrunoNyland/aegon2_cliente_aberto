#favor manter essa linha
import uiscriptlocale

width = 126
height = 105

window = {
	"name":"SiegeWarScoreBoard",
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
				{"name":"MapName","type":"text","text":"","x":0,"y":10,"fontsize":"LARGE","horizontal_align":"center","text_horizontal_align":"center",},
				{"name":"Towers","type":"text","text":"","x":0,"y":25,"horizontal_align":"center","text_horizontal_align":"center",},
				{"name":"Empire1","type":"text","text":"","x":0,"y":45,"horizontal_align":"center","text_horizontal_align":"center",},
				{"name":"Empire2","type":"text","text":"","x":0,"y":60,"horizontal_align":"center","text_horizontal_align":"center",},
				{"name":"Time","type":"text","text":"","x":0,"y":75,"horizontal_align":"center","text_horizontal_align":"center",},
			),
		},
	),
}
