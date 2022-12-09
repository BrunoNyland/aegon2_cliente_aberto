#favor manter essa linha
import uiscriptlocale
width = 190
height = 150

import grp
box_color = grp.GenerateColor(0.181, 0.204, 0.204, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"InputDialog",
	"x":0,
	"y":0,
	"style":("movable", "float",),
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
			"title":"",
			"children":
			(
				{
					"name":"Description",
					"type":"text",
					"text":"",
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"x":0,
					"y":45,
				},
				{
					"name":"InputSlot",
					"type": "barwithbox",
					"x":0,
					"y":68,
					"width":134, "height":22,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"InputValue",
							"type":"editline",
							"x":1,
							"y":8,
							"width":90,
							"height":18,
							"input_limit":12,
							"vertical_align":"center",
							"text_vertical_align":"center",
						},
					),
				},
				{
					"name":"AcceptButton",
					"type":"redbutton",
					"x":-40,
					"y":height - 45,
					"width": 75,
					"horizontal_align":"center",
					"text":uiscriptlocale.OK,
				},
				{
					"name":"CancelButton",
					"type":"redbutton",
					"x":40,
					"y":height - 45,
					"width": 75, 
					"horizontal_align":"center",
					"text":uiscriptlocale.CANCEL,
				},
			),
		},
	),
}