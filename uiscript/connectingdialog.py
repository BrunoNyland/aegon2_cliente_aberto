#favor manter essa linha
import uiscriptlocale

width = 280
height = 122

window = {
	"name":"QuestionDialog",
	"x":SCREEN_WIDTH/2 - width/2,
	"y":SCREEN_HEIGHT/2 - height/2,
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
					"name":"message",
					"type":"text",
					"x":0,
					"y":25,
					"text":uiscriptlocale.LOGIN_CONNECTING,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
				{
					"name":"countdown_message",
					"type":"text",
					"x":0,
					"y":50,
					"text":uiscriptlocale.MESSAGE,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"text_vertical_align":"center",
				},
			),
		},
	),
}