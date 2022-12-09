#favor manter essa linha
import uiscriptlocale
width = 340
height = 105

window = {
	"name":"ItemQuestionDialog",
	"style":("movable", "float",),
	"x":SCREEN_WIDTH/2 - 125,
	"y":SCREEN_HEIGHT/2 - 52,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"title":"",
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"message",
					"type":"text",
					"x":60,
					"y":48,
					"text":uiscriptlocale.MESSAGE,
				},
				{
					"name":"separator",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 60,
				},
				{
					"name":"vseparator",
					"type":"verticalseparator",
					"height":32,
					"x":12 + 32 +1,
					"y":38,
				},
				{
					"name":"accept",
					"type":"redbutton",
					"x":-50,
					"y":height - 47,
					"width":90,
					"horizontal_align":"center",
					"text":uiscriptlocale.YES,
				},
				{
					"name":"cancel",
					"type":"redbutton",
					"x":50,
					"y":height - 47,
					"width":90,
					"horizontal_align":"center",
					"text":uiscriptlocale.NO,
				},
			),
		},
	),
}