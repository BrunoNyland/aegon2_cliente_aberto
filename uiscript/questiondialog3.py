#favor manter essa linha
import uiscriptlocale

window = {
	"name":"QuestionDialog",
	"style":("movable", "float",),
	"x":SCREEN_WIDTH/2 - 125,
	"y":SCREEN_HEIGHT/2 - 52,
	"width":280,
	"height":130,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"x":0,
			"y":0,
			"width":280,
			"height":130,
			"children":
			(
				{
					"name":"message1",
					"type":"text",
					"x":0,
					"y":20,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"message2",
					"type":"text",
					"x":0,
					"y":20+16,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"message3",
					"type":"text",
					"x":0,
					"y":20+16*2,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"accept",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":-50,
					"y":89,
					"width": 70,
					"text":uiscriptlocale.YES,
				},
				{
					"name":"cancel",
					"type":"redbutton",
					"horizontal_align":"center",
					"x":50,
					"y":89,
					"width": 70,
					"text":uiscriptlocale.NO,
				},
			),
		},
	),
}