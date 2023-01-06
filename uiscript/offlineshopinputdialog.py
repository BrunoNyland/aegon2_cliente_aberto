#favor manter essa linha
import uiscriptlocale

width = 290
height = 160

LINE = "interface/controls/common/horizontal_bar/center.tga"

import _grp as grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"OfflineShopInputDialog",
	"style":("movable", "float",),
	"x":0,
	"y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"style":("attach",),
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Escolha um nome para a Loja",
			"children":
			(
				{
					"name":"",
					"type":"expanded_image",
					"image":LINE,
					"x":0,
					"y":40,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"inputtitle",
							"type":"text",
							"text":"Digite o Nome",
							"x":0,
							"y":-5,
							"all_align":"center",
						},
					),
				},
				{
					"name":"InputSlot",
					"type": "barwithbox",
					"width":220, "height":27,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":69,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"InputValue",
							"type":"editline",
							"vertical_align":"center",
							"text_vertical_align":"center",
							"x":3,
							"y":6,
							"width":235,
							"height":15,
							"input_limit":23,
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
					"name":"AgreeButton",
					"type":"redbutton",
					"x":0,
					"y":height - 47,
					"horizontal_align":"center",
					"width":80,
					"text":"Aceitar",
				},
				{
					"name":"CancelButton",
					"type":"redbutton",
					"x":85,
					"y":height - 47,
					"horizontal_align":"center",
					"width":80,
					"text":"Cancelar",
				},
			),
		},
	),
}