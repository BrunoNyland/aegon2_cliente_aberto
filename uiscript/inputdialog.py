#favor manter essa linha
import uiscriptlocale
width = 190
height = 124

import _grp as grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
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
					"name":"InputSlot",
					"type": "barwithbox",
					"x":0,
					"y":45,
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