import uiscriptlocale

width = 170
height = 130

import grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"AmountDialog",
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
					"name":"InputSlot",
					"type":"expanded_image",
					"type": "barwithbox",
					"width":88, "height":28,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":41,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"Minus",
							"type":"button",
							"x":-30,
							"y":0,
							"horizontal_align":"center",
							"vertical_align":"center",
							"default_image":"interface/controls/common/button_status/minus_n.tga",
							"over_image":"interface/controls/common/button_status/minus_h.tga",
							"down_image":"interface/controls/common/button_status/minus_n.tga",
							"disable_image":"interface/controls/common/button_status/minus_a.tga",
						},
						{
							"name":"Plus",
							"type":"button",
							"x":30,
							"y":0,
							"horizontal_align":"center",
							"vertical_align":"center",
							"default_image":"interface/controls/common/button_status/plus_n.tga",
							"over_image":"interface/controls/common/button_status/plus_h.tga",
							"down_image":"interface/controls/common/button_status/plus_n.tga",
							"disable_image":"interface/controls/common/button_status/plus_a.tga",
						},
						{
							"name":"amount_value",
							"type":"editline",
							"x":27,
							"y":7,
							"width":30,
							"height":18,
							"input_limit":4,
							"only_number":1,
							"color":0xffffffff,
							"fontsize":"LARGE",
							"vertical_align":"center",
							"text_vertical_align":"center",
							"text":"1",
						},
					),
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 60,
				},
				{
					"name":"accept_button",
					"type":"redbutton",
					"x":-35,
					"y":height - 47,
					"horizontal_align":"center",
					"width":68,
					"text":"Aceitar",
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"x":35,
					"y":height - 47,
					"horizontal_align":"center",
					"width":68,
					"text":"Cancelar",
				},
			),
		},
	),
}