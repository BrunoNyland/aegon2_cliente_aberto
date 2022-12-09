#favor manter essa linha
import uiscriptlocale

width = 280
height = 105

window = {
	"name":"QuestionDialog",
	"style":("movable", "float",),
	"x":SCREEN_WIDTH/2 - 125,
	"y":SCREEN_HEIGHT/2 - 52,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"message1",
					"type":"text",
					"x":0,
					"y":25,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"message2",
					"type":"text",
					"x":0,
					"y":40,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"accept",
					"type":"redbutton",
					"x":-50,
					"y":height - 30,
					"width":80,
					"horizontal_align":"center",
					"text":uiscriptlocale.YES,
				},
				{
					"name":"cancel",
					"type":"redbutton",
					"x":50,
					"y":height - 30,
					"width":80,
					"horizontal_align":"center",
					"text":uiscriptlocale.NO,
				},
			),
		},
	),
}