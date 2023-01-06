#favor manter essa linha
import uiscriptlocale
import _grp as grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

SLOT = "interface/controls/common/slot_rectangle/slot.tga"

width = 176
height = 390

window = {
	"name":"PrivateShopBuilder",
	"x":0,
	"y":0,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"style":("attach",),
			"title":uiscriptlocale.PRIVATE_SHOP_TITLE,
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"NameSlot",
					"type": "barwithbox",
					"width":156, "height":28,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":height - 348,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"NameLine",
							"type":"text",
							"x":1,
							"y":-1,
							"width":width,
							"height":15,
							"input_limit":16,
							"text":"OOOOOOOOOOOOOOOOO",
							"vertical_align":"center",
							"text_vertical_align":"center",
						},
					),
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height-314-4,
				},
				{
					"name":"ItemSlot",
					"type":"grid_table",
					"x":8,
					"y":height-314,
					"start_index":0,
					"x_count":5,
					"y_count":8,
					"x_step":32,
					"y_step":32,
					"image":SLOT,
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 60,
				},
				{
					"name":"OkButton",
					"type":"redbutton",
					"x":-38,
					"y":height - 47,
					"horizontal_align":"center",
					"width":65,
					"text":uiscriptlocale.OK,
				},
				{
					"name":"CloseButton",
					"type":"redbutton",
					"x":38,
					"y":height - 47,
					"horizontal_align":"center",
					"width":65,
					"text":uiscriptlocale.CLOSE,
				},
			),
		},
	),
}