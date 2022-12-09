#favor manter essa linha
import uiscriptlocale
width = 210
height = 110

import grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"PickMoneyDialog",
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
			"title":"Digite o Valor",
			"children":
			(
				{
					"name":"money_slot",
					"type": "barwithbox",
					"width":176, "height":22,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":42,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"",
							"type": "barwithbox",
							"width":176/2, "height":22,
							"color": normal_color,
							"flash_color": normal_color,
							"box_color": box_color,
							"x":0,
							"y":0,
						},
						{
							"name":"money_value",
							"type":"editline",
							"x":1,
							"y":8,
							"width":60,
							"height":18,
							"input_limit":6,
							# "only_number":1,
							"money_mode":1,
							"text":"1",
							"vertical_align":"center",
							"text_vertical_align":"center",
						},
						{
							"name":"max_value",
							"type":"text",
							"x":92,
							"y":-1,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"text":"99999999999",
							"color":box_color,
						},
					),
				},
				{
					"name":"accept_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"width": 70,
					"x":-45,
					"y":height-35,
					"text":uiscriptlocale.OK,
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"horizontal_align":"center",
					"width": 70,
					"x":45,
					"y":height-35,
					"text":uiscriptlocale.CANCEL,
				},
			),
		},
	),
}