#favor manter essa linha
import uiscriptlocale

width = 170
height = 120

import _grp as grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"PickEtcDialog",
	"x":100,
	"y":100,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Quantidade",
			"children":
			(
				{
					"name":"etc_slot",
					"type": "barwithbox",
					"width":120, "height":22,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":45,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"",
							"type": "barwithbox",
							"width":120/2, "height":22,
							"color": normal_color,
							"flash_color": normal_color,
							"box_color": box_color,
							"x":60,
							"y":0,
							"children":
							(
								{
									"name":"max_value",
									"type":"text",
									"y":-1,
									"x":5,
									"vertical_align":"center",
									"text_vertical_align":"center",
									"color":box_color,
									"text":"999999",
								},
							),
						},
						{
							"name":"etc_value",
							"type":"editline",
							"x":1,
							"y":8,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"width":110,
							"height":18,
							"input_limit":6,
							"only_number":1,
							"text":"1",
						},
					),
				},
				{
					"name":"accept_button",
					"type":"redbutton",
					"x":-38,
					"y":height - 40,
					"horizontal_align":"center",
					"width":65,
					"text":uiscriptlocale.OK,
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"x":38,
					"y":height - 40,
					"horizontal_align":"center",
					"width":65,
					"text":uiscriptlocale.CLOSE,
				},
			),
		},
	),
}