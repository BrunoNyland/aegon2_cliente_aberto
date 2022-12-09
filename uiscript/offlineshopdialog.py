#favor manter essa linha
import uiscriptlocale

width = 176
height = 303

SLOT = "interface/controls/common/slot_rectangle/slot.tga"

window = {
	"name":"OfflineShopDialog",
	"x":SCREEN_WIDTH - 400,
	"y":10,
	"style":("movable", "float",),
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
			"title":uiscriptlocale.SHOP_TITLE,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"ItemSlot",
					"type":"grid_table",
					"x":8,
					"y":39,
					"start_index":0,
					"x_count":5,
					"y_count":8,
					"x_step":32,
					"y_step":32,
					"image":SLOT,
				},
			),
		},
	),
}