#favor manter essa linha
import uiscriptlocale

window = {
	"name":"PopupDialog",
	"style":("float",),
	"x":SCREEN_WIDTH/2 - 250,
	"y":SCREEN_HEIGHT/2 - 40,
	"width":280,
	"height":105,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"x":0,
			"y":0,
			"width":280,
			"height":105,
			"children":
			(
				{
					"name":"message",
					"type":"text",
					"x":0,
					"y":38,
					"r":1.0,
					"g":0.85,
					"b":0.65,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"accept",
					"type":"redbutton",
					"x":0,
					"y":63,
					"width":70,
					"horizontal_align":"center",
					"text":uiscriptlocale.OK,
				},
			),
		},
	),
}