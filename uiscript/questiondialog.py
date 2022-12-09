#favor manter essa linha
import uiscriptlocale

window = {
	"name":"QuestionDialog",
	"style":("movable", "float",),
	"x":SCREEN_WIDTH/2 - 125,
	"y":SCREEN_HEIGHT/2 - 52,
	"width":340,
	"height":105,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"x":0,
			"y":0,
			"width":340,
			"height":105,
			"children":
			(
				{
					"name":"message",
					"type":"text",
					"x":0,
					"y":38,
					"horizontal_align":"center",
					"text":uiscriptlocale.MESSAGE,
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"accept",
					"type":"redbutton",
					"x":-40,
					"y":63,
					"width":70,
					"horizontal_align":"center",
					"text":uiscriptlocale.YES,
				},
				{
					"name":"cancel",
					"type":"redbutton",
					"x":40,
					"y":63,
					"width":70,
					"horizontal_align":"center",
					"text":uiscriptlocale.NO,
				},
			),
		},
	),
}